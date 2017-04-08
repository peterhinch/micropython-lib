import uasyncio as asyncio
import utime as time
import pyb

tmax = 0
tmin = 1000000

async def report(secs):
    count = 0
    while True:
        await asyncio.sleep(secs)
        count += secs
        print('{} t = {:5.1f}ms max {:5.1f}ms min'.format(count, tmax / 1000, tmin / 1000))

async def lp_task(x):
    while True:
        await asyncio.low_priority
        time.sleep_us(int((5 + pyb.rng()/2**27) * 40)) # Simulate processing: block 200-520us

async def priority(ms):
    global tmax, tmin
    while True:
        tstart = time.ticks_us()
        await asyncio.sleep_ms(ms)  # Time critical
        delta = time.ticks_diff(time.ticks_us(), tstart)
        tmax = max(tmax, delta)
        tmin = min(tmin, delta)


loop = asyncio.get_event_loop()
loop.create_task(report(10))
loop.create_task(priority(10))
for x in range(10):
    loop.create_task(lp_task(x))
loop.run_forever()
