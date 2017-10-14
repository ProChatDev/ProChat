import websockets
import asyncio
import json

config = {}

connected = set()

with open("config.json") as json_data:
	config = json.loads(json_data.read())
	json_data.close()

connected_payload = {
	"message": "Welcome, please send your authentication message within 10 seconds",
	"code": 1
}

async def handler(websocket, path):
	global connected

	await websocket.send(json.dumps(connected_payload))

	try:
		msg = await asyncio.wait_for(receive_from_ws(websocket), timeout=10)
		if msg == None:
			await close_on_connect(websocket)
			return

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

async def send(ws, message):
	await ws.send(json.dumps(message))

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