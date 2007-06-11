from zope.i18nmessageid import Message

I18nMessageTypes = (Message,)
TypesToTranslate = I18nMessageTypes + (str, unicode)

def isI18nMessageTypes(value):
    return isinstance(value, I18nMessageTypes)

def isTypesToTranslate(value):
    return isinstance(value, TypesToTranslate)

