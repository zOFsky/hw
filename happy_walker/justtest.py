# test.py
def application(env, start_response):
    start_response('200 OK', [('Content-Type','text/html')])
    return [b"Hello HURRAY!!!! WORLD!!!!"] # python3
    #return ["Hello World"] # python2