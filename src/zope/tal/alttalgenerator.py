from zope.tal.talgenerator import TALGenerator

class AltTALGenerator(TALGenerator):

    def __init__(self, repldict, expressionCompiler=None, xml=0):
        self.repldict = repldict
        self.enabled = 1
        TALGenerator.__init__(self, expressionCompiler, xml)

    def enable(self, enabled):
        self.enabled = enabled

    def emit(self, *args):
        if self.enabled:
            TALGenerator.emit(self, *args)

    def emitStartElement(self, name, attrlist, taldict, metaldict, i18ndict,
                         position=(None, None), isend=0):
        metaldict = {}
        taldict = {}
        i18ndict = {}
        if self.enabled and self.repldict:
            taldict["attributes"] = "x x"
        TALGenerator.emitStartElement(self, name, attrlist,
                                      taldict, metaldict, i18ndict,
                                      position, isend)

    def replaceAttrs(self, attrlist, repldict):
        if self.enabled and self.repldict:
            repldict = self.repldict
            self.repldict = None
        return TALGenerator.replaceAttrs(self, attrlist, repldict)

