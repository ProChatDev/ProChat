import websockets
import asyncio
import json
import pymongo

config = {}

connected = set()

with open("config.json") as json_data:
	config = json.loads(json_data.read())
	json_data.close()

db_client = pymongo.MongoClient(config.get("mongo_uri", "mongodb://localhost:27017/"))
db = db_client[config.get('mongo_database_name', "prochat")]
users = db.users
messages = db.messages

connected_payload = {
	"message": "Welcome, please send your authentication token within 10 seconds",
	"code": 1
}

async def register_message(pkt, socket):
	if not isinstance(pkt, dict):
		return
	if not 'content' in pkt:
		return
	content = pkt.get("content")
	if not content:
		return
	data = {}
	data['timestamp'] = int(round(time.time() * 1000))
	data['_id'] = generate_id()
	data['sender_id'] = socket.user['_id']
	data['content'] = content
	messages.insert_one(data)
	await send_to_all(json.dumps(data))


def generate_id():
    import time
    f = 1508320834
    f2 = int(round(time.time() * 1000))
    return ((f2 - f) << 10) + ((1<<10)-0)


async def handler(websocket, path):
	global connected

	await websocket.send(json.dumps(connected_payload))

	try:
		msg = await asyncio.wait_for(receive_from_ws(websocket), timeout=10)
		if msg == None:
			await close_on_connect(websocket)
			return
		if not "token" in msg:
			return await close_on_connect(websocket)
		token = msg.get("token")
		user = users.find_one({"token":token})
		if not user:
			return await invalid_token(websocket)
		websocket.user = user
		await send(websocket, {"message":"You have successfully authenticated, you may now start sending messages!", "code":4})

	except asyncio.TimeoutError:
		await close_on_connect(websocket)
		return
	except websockets.exceptions.ConnectionClosed:
		return

	connected.add(websocket)

	while True:
		msg = await receive_from_ws(websocket)
		if msg is None:
			break
		register_message(msg, websocket)

async def send(ws, message):
	await ws.send(json.dumps(message))

async def invalid_token(ws):
	invalid_token_payload = {
		"message": "Invalid token",
		"code": 3
	}
	await send(ws, invalid_token_payload)
	try:
		await ws.close(code=1001, reason="Forbidden")
	except:
		pass

async def close_on_connect(ws):
	disconnected_payload = {
		"message": "Not authenticated in time",
		"code": 2
	}
	await send(ws, disconnected_payload)
	try:
		await ws.close(code=1001, reason="Unauthenticated")
	except:
		pass

async def receive_from_ws(ws):
	try:
		msg = await ws.recv()
		try:
			jsonn = json.loads(msg)
			return jsonn
		except:
			return None
	except websockets.exceptions.ConnectionClosed:
		try:
			connected.remove(ws)
		except:
			pass
		return None
	except:
		return None

async def send_to_all(message):
	for ws in connected:
		try:
			await ws.send(message)
		except:
			pass
			connected.remove(ws)

start_server = websockets.serve(handler, '', config.get("port", 4000))

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
