from asyncua import ua, Server
import asyncio
import random

async def main():
    server = Server()
    await server.init()
    server.set_endpoint("opc.tcp://0.0.0.0:4840/freeopcua/server/")

    uri = "http://examples.freeopcua.github.io"
    idx = await server.register_namespace(uri)

    # ✅ These now require `await` in 1.x
    objects_node = await server.nodes.objects
    myobj = await objects_node.add_object(idx, "MyObject")

    temp_var = await myobj.add_variable(idx, "Temperature", 0.0)
    hum_var = await myobj.add_variable(idx, "Humidity", 0.0)

    await temp_var.set_writable()
    await hum_var.set_writable()

    async with server:
        while True:
            temp = random.uniform(20.0, 25.0)
            hum = random.uniform(30.0, 50.0)

            await temp_var.write_value(temp)
            await hum_var.write_value(hum)

            print(f"Temperature: {temp:.2f}, Humidity: {hum:.2f}")
            await asyncio.sleep(1)

asyncio.run(main())
