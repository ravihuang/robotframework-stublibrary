from .robotlibcore import keyword

class SIP(object):
    @staticmethod
    @keyword
    def hello_sip(msg):
        print 'hello SIP'