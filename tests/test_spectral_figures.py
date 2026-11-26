from io import BytesIO
import numpy as np
from PIL import Image
from spectral_figures import publication_bytes

def test_publication_formats_and_dpi():
    # Synthetic curve for renderer testing only, not a demo or experimental result.
    x=np.linspace(1003,3891,750)
    y=np.sin(x/200)
    args=(x,[("Query",y),("Reference",y*.8)],"Normalized first derivative",True,(1003.,3891.),None,2.,("#111111","#C43C35"),True)
    png=publication_bytes(*args,"png")
    im=Image.open(BytesIO(png))
    assert abs(im.info["dpi"][0]-600)<1
    assert abs(im.width-130/25.4*600)<3
    assert abs(im.height-100/25.4*600)<3
    assert publication_bytes(*args,"pdf").startswith(b"%PDF")
    assert b"<svg" in publication_bytes(*args,"svg")
