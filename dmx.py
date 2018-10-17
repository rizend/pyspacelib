from httpish import POST200
import json

base = "http://10.20.0.49:9090"
default_universe = 1

def set_dmx(vals, universe=default_universe, base=base):
  if len(vals) != 512:
    raise ValueError("DMX512 only supported")
  set_dmx_endpoint = "/set_dmx"
  payload = {
    "u": universe,
    "d": ','.join(map(str, vals))
  }
  return POST200(base+set_dmx_endpoint, payload)

def blackout(universe=default_universe, base=base):
  return set_dmx([0]*512, universe=universe, base=base)

