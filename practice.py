suffixList = ['acy','ance','ence','ism','ist','ity','ty',
              'ment','ness','ship','sion','tion','ate','ify','fy','ize',
              'ise','able','ible','esque','ful','ic','ical','ious','ous',
              'ish','ive','less']


def removeSuffix(strg):
    for suffix in suffixList:
        if strg.endswith(suffix):
            strg = strg[:-len(suffix)]
    return strg
        
sampleStr = "loyalty"
sampleStr = removeSuffix(sampleStr)
print(sampleStr)
