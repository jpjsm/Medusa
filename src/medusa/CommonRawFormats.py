from pydantic import BaseModel

class RawFormatInfo(BaseModel):
    Extension: str
    Description: str
    Maker: str

COMMON_RAW_FORMATS = [
    RawFormatInfo(Extension='.DNG', Description='Apple ProRAW Image', Maker='Apple'),
    RawFormatInfo(Extension='.ARI', Description='ARRIRAW Image', Maker='ARRIRAW'),
    RawFormatInfo(Extension='.CR2', Description='Canon Raw 2 Image', Maker='Canon'),
    RawFormatInfo(Extension='.CRW', Description='Canon Raw CIFF Image File', Maker='Canon'),
    RawFormatInfo(Extension='.CR3', Description='Canon Raw 3 Image', Maker='Canon'),
    RawFormatInfo(Extension='.CS1', Description='CaptureShop 1-shot Raw Image', Maker='CaptureShop'),
    RawFormatInfo(Extension='.BAY', Description='Casio RAW Image', Maker='Casio'),
    RawFormatInfo(Extension='.DNG', Description='Digital Negative Image', Maker='Digital'),
    RawFormatInfo(Extension='.ERF', Description='Epson RAW File', Maker='Epson'),
    RawFormatInfo(Extension='.RAF', Description='Fujifilm RAW Image', Maker='Fujifilm'),
    RawFormatInfo(Extension='.GPR', Description='GoPro RAW Image', Maker='GoPro'),
    RawFormatInfo(Extension='.3FR', Description='Hasselblad 3F RAW Image', Maker='Hasselblad'),
    RawFormatInfo(Extension='.FFF', Description='Hasselblad RAW Image', Maker='Hasselblad'),
    RawFormatInfo(Extension='.DCR', Description='Kodak Digital Camera RAW Image', Maker='Kodak'),
    RawFormatInfo(Extension='.K25', Description='Kodak DC25 Digital Photo', Maker='Kodak'),
    RawFormatInfo(Extension='.KC2', Description='Kodak DCS200 Camera Raw Image', Maker='Kodak'),
    RawFormatInfo(Extension='.KDC', Description='Kodak Photo-Enhancer File', Maker='Kodak'),
    RawFormatInfo(Extension='.MOS', Description='Leaf Camera RAW Image', Maker='Leaf'),
    RawFormatInfo(Extension='.RWL', Description='Leica RAW Image', Maker='Leica'),
    RawFormatInfo(Extension='.MEF', Description='Mamiya RAW Image', Maker='Mamiya'),
    RawFormatInfo(Extension='.MFW', Description='Mamiya Camera Raw File', Maker='Mamiya'),
    RawFormatInfo(Extension='.MRW', Description='Minolta Raw Image', Maker='Minolta'),
    RawFormatInfo(Extension='.MDC', Description='Minolta Camera Raw Image', Maker='Minolta'),
    RawFormatInfo(Extension='.NRW', Description='Nikon Raw Image', Maker='Nikon'),
    RawFormatInfo(Extension='.NEF', Description='Nikon Electronic Format RAW Image', Maker='Nikon'),
    RawFormatInfo(Extension='.NKSC', Description='Nikon Capture NX-D Sidecar File', Maker='Nikon'),
    RawFormatInfo(Extension='.ORF', Description='Olympus RAW File', Maker='Olympus'),
    RawFormatInfo(Extension='.RW2', Description='Panasonic RAW Image', Maker='Panasonic'),
    RawFormatInfo(Extension='.PEF', Description='Pentax Electronic File', Maker='Pentax'),
    RawFormatInfo(Extension='.EIP', Description='Enhanced Image Package File', Maker='Phase'),
    RawFormatInfo(Extension='.IIQ', Description='Phase One RAW Image', Maker='Phase'),
    RawFormatInfo(Extension='.RAW', Description='Raw Image Data', Maker='Raw'),
    RawFormatInfo(Extension='.RWZ', Description='Rawzor Compressed Image', Maker='Rawzor'),
    RawFormatInfo(Extension='.J6I', Description='Ricoh Camera Image File', Maker='Ricoh'),
    RawFormatInfo(Extension='.SRW', Description='Samsung RAW Image', Maker='Samsung'),
    RawFormatInfo(Extension='.X3F', Description='SIGMA X3F Camera RAW File', Maker='SIGMA'),
    RawFormatInfo(Extension='.ARW', Description='Sony Alpha Raw Digital Camera Image', Maker='Sony'),
    RawFormatInfo(Extension='.SR2', Description='Sony RAW Image', Maker='Sony'),
    RawFormatInfo(Extension='.SRF', Description='Sony RAW Image', Maker='Sony'),
]