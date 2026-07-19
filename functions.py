import json
import random
import ssl
import urllib
import uuid

import paho.mqtt.client as mqtt

import variables

broker = "broker.emqx.io"
port = 8084

app_topic_root = f"{variables.app_name}-aposjdnajwioajsndkalsdjnaksdj"

client: mqtt.Client | None = None
session_code: str | None = None
client_id: str = uuid.uuid4().hex[:12]
my_name: str | None = None
members: dict[str, dict] = {}
ready: set[str] = set()
round_started: bool = False
on_member_update = None
on_round_start = None


def session_topic(code: str) -> str:
    return f"{app_topic_root}/{code}"


def notify_member_update():
    if on_member_update is not None:
        on_member_update()


def recompute_display_names():
    seen_counts: dict[str, int] = {}
    for cid in sorted(members.keys()):
        base_name = members[cid]["name"]
        seen_counts[base_name] = seen_counts.get(base_name, 0) + 1
        n = seen_counts[base_name]
        members[cid]["display_name"] = base_name if n == 1 else f"{base_name} ({n})"


def get_members() -> dict[str, dict]:
    return dict(members)


def get_my_display_name() -> str | None:
    entry = members.get(client_id)
    return entry["display_name"] if entry else None


def on_connect(client, userdata, flags, reason_code, properties=None):
    if reason_code == 0:
        print(f"[net] connected to {broker}:{port} as {client_id}")
        if session_code is not None:
            client.subscribe(session_topic(session_code))
            print(f"[net] listening on session '{session_code}'")
            if my_name is not None:
                announce_self("hello")
    else:
        print(f"[net] connection failed: {reason_code}")


def on_disconnect(client, userdata, reason_code, properties=None, *args):
    print(f"[net] disconnected ({reason_code})")


def on_message(client, userdata, msg):
    try:
        payload = json.loads(msg.payload.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError):
        payload = msg.payload
    if not isinstance(payload, dict):
        print(f"[net] message on '{msg.topic}': {payload}")
        return
    msg_type = payload.get("type")
    sender = payload.get("sender")
    if msg_type == "hello" and sender is not None:
        register_member(sender, payload.get("name", "Player"))
        if sender != client_id and my_name is not None:
            announce_self("here")
    elif msg_type == "here" and sender is not None:
        register_member(sender, payload.get("name", "Player"))
    elif msg_type == "bye" and sender is not None:
        if sender in members:
            del members[sender]
            ready.discard(sender)
            recompute_display_names()
            notify_member_update()
    elif msg_type == "ready" and sender is not None:
        if sender in members and sender not in ready:
            ready.add(sender)
            notify_member_update()
            check_round_start()
    else:
        if sender == client_id:
            return
        print(f"[net] message on '{msg.topic}': {payload}")


def register_member(cid: str, name: str):
    is_new = cid not in members
    changed_name = (not is_new) and members[cid]["name"] != name
    if is_new or changed_name:
        members[cid] = {"name": name, "display_name": name}
        recompute_display_names()
        notify_member_update()


def announce_self(msg_type: str):
    client.publish(session_topic(session_code), json.dumps({"type": msg_type, "sender": client_id, "name": my_name}))


def check_round_start():
    global round_started
    if round_started or not members:
        return
    if len(ready) / len(members) >= 0.5:
        round_started = True
        if on_round_start is not None:
            on_round_start()


def vote_start() -> None:
    if client is None or session_code is None:
        raise RuntimeError("join_lobby() must be called before vote_start()")
    if client_id in ready:
        return
    ready.add(client_id)
    announce_self("ready")
    notify_member_update()
    check_round_start()


def get_ready_count() -> tuple[int, int]:
    return len(ready), len(members)


def connect(code: str, blocking: bool = False) -> mqtt.Client:
    global client, session_code
    session_code = str(code)
    new_client = mqtt.Client(client_id=client_id, callback_api_version=mqtt.CallbackAPIVersion.VERSION2,
                             transport="websockets")
    new_client.ws_set_options(path="/mqtt")
    new_client.tls_set(cert_reqs=ssl.CERT_REQUIRED)
    new_client.on_connect = on_connect
    new_client.on_disconnect = on_disconnect
    new_client.on_message = on_message
    try:
        if blocking:
            new_client.connect(broker, port, keepalive=60)
        else:
            new_client.connect_async(broker, port, keepalive=60)
    except OSError as exc:
        raise ConnectionError(
            f"Could not reach {broker}:{port}. This is usually a firewall, antivirus, or network policy blocking the outbound connection - check your firewall/antivirus settings, or try a different network (e.g. mobile hotspot) to confirm.") from exc
    if blocking:
        new_client.loop_forever()
    else:
        new_client.loop_start()
    client = new_client
    return client


def join_lobby(code: str, name: str, blocking: bool = False) -> mqtt.Client:
    global my_name, round_started
    my_name = name
    members.clear()
    ready.clear()
    round_started = False
    c = connect(code, blocking=blocking)
    register_member(client_id, my_name)
    return c


def leave_lobby() -> None:
    global round_started
    if client is not None and session_code is not None and my_name is not None:
        announce_self("bye")
    disconnect()
    members.clear()
    ready.clear()
    round_started = False


def send(data) -> None:
    if client is None or session_code is None:
        raise RuntimeError("connect() must be called before send()")
    if isinstance(data, dict):
        payload = {**data, "sender": client_id}
    else:
        payload = {"sender": client_id, "data": data}
    client.publish(session_topic(session_code), json.dumps(payload))


def disconnect() -> None:
    global client, session_code, my_name
    if client is not None:
        client.loop_stop()
        client.disconnect()
    client = None
    session_code = None
    my_name = None


def set_text_color(widget, color):
    widget.configure(active_unpressed_text_color=color, active_hover_text_color=color, active_pressed_text_color=color,
                     disabled_unpressed_text_color=color, disabled_hover_text_color=color)

def get_album_art(track_url=None):
    if not track_url:
        track_url=random.choice([
            "https://open.spotify.com/track/4uLU6hMCjMI75M1A2tKUQC",
            "https://open.spotify.com/track/3Nl5OkkmS5DaBZvuYofpAt",
            "https://open.spotify.com/track/5CZ40GBx1sQ9agT82CLQCT",
            "https://open.spotify.com/track/53iuhJlwXhSER5J2IYYv1W",
            "https://open.spotify.com/track/1BxfuPKGuaTgP7aM0Bbdwr",
            "https://open.spotify.com/track/1R0a2iXumgCiFb7HEZ7gUE",
            "https://open.spotify.com/track/5YqltLsjdqFtvqE7Nrysvs",
            "https://open.spotify.com/track/1ZVp3jxaSfx1eket9duUkZ",
            "https://open.spotify.com/track/6XVSsVuzVUZ2zgRWB5xwef",
            "https://open.spotify.com/track/5qrSlOut2rNAWv3ubArkNy",
            "https://open.spotify.com/track/2VyOhGV0rwqHuCribVSutf",
            "https://open.spotify.com/track/7ygpwy2qP3NbrxVkHvUhXY",
            "https://open.spotify.com/track/1GhbQDYGEOjyFwfT8lojcx",
            "https://open.spotify.com/track/49j6SvuvWfbEKZKzsHCdLJ",
            "https://open.spotify.com/track/3BovdzfaX4jb5KFQwoPfAw",
            "https://open.spotify.com/track/1rIKgCH4H52lrvDcz50hS8",
            "https://open.spotify.com/track/6dOtVTDdiauQNBQEDOtlAB",
            "https://open.spotify.com/track/3QGsuHI8jO1Rx4JWLUh9jd",
            "https://open.spotify.com/track/7ne4VBA60CxGM75vw0EYad",
            "https://open.spotify.com/track/4nyF5lmSziBAt7ESAUjpbx",
            "https://open.spotify.com/track/3di5hcvxxciiqwMH1jarhY"
        ])
    encoded_url = urllib.parse.quote(track_url)
    oembed_endpoint = f"https://open.spotify.com/oembed?url={encoded_url}"
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
    try:
        req = urllib.request.Request(oembed_endpoint, headers=headers)
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode())
        image_url = data.get("thumbnail_url")
        if not image_url:
            print("Fehler: Kein Cover im Spotify-Link gefunden.")
            return
        img_req = urllib.request.Request(image_url, headers=headers)
        with urllib.request.urlopen(img_req) as img_response:
            with open("assets/cover.png", 'wb') as f:
                f.write(img_response.read())
        print(f"Erfolgreich heruntergeladen")
    except Exception as e:
        print(f"Ein Fehler ist aufgetreten: {e}")