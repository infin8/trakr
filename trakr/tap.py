from twisted.web import server, static
from twisted.application import service, internet
from twisted.python import usage

from twisted.web.wsgi import WSGIResource
from twisted.web.resource import Resource
from twisted.internet import reactor


from wsgi import application

class SharedRoot(Resource):
    """Root resource that combines the two sites/entry points"""
    wsgi = None

    def getChild(self, child, request):
        request.prepath.pop()
        request.postpath.insert(0, child)
        return self.wsgi

    def render(self, request):
        return self.wsgi.render(request)
        
class Options(usage.Options):    
    optParameters = [
        ['ip', 'i', 'localhost', 'ip to bind to'],
        ['port', 'p', 8101, 'port to bind to']
    ]

def getSite():
    root = SharedRoot()
    
    resource = WSGIResource(reactor, reactor.getThreadPool(), application)

    root.wsgi = resource
    
    return server.Site(root)
    
def makeService(config):
    site = getSite()
    return internet.TCPServer(int(config['port']), site,
                              interface=config['ip'])
