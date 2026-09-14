from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from .config import ASSETS_DIR, DEFAULT_FONT_SIZE

WARM_BROWN = (90, 64, 48, 255)
CREAM = (255, 250, 241, 244)
LABEL_BG = (239, 229, 211, 246)
THOUGHT_BG = (250, 247, 240, 242)


def choose_font():
    candidates = []
    candidates += sorted((ASSETS_DIR / "fonts").glob("*.ttf"))
    candidates += sorted((ASSETS_DIR / "fonts").glob("*.otf"))
    candidates += sorted((ASSETS_DIR / "fonts").glob("*.ttc"))
    fallbacks = [
        Path("C:/Windows/Fonts/malgun.ttf"),
        Path("/usr/share/fonts/truetype/nanum/NanumSquareRoundR.ttf"),
        Path("/usr/share/fonts/truetype/nanum/NanumGothic.ttf"),
        Path("/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc"),
    ]
    candidates += [p for p in fallbacks if p.exists()]
    return candidates[0] if candidates else None


def _font(size):
    p = choose_font()
    if not p:
        return ImageFont.load_default()
    return ImageFont.truetype(str(p), size=size)


def wrap_text(draw, text, font, max_width):
    lines=[]
    for paragraph in str(text).split("\n"):
        if not paragraph:
            lines.append("")
            continue
        cur=""
        for ch in paragraph:
            test=cur+ch
            if draw.textbbox((0,0), test, font=font)[2] <= max_width or not cur:
                cur=test
            else:
                lines.append(cur)
                cur=ch
        lines.append(cur)
    return lines[:3]


def _layout(item: dict, width: int):
    typ=item.get("type","dialogue")
    size=int(item.get("font_size", DEFAULT_FONT_SIZE.get(typ, 52)))
    font=_font(size)
    padding_x=int(item.get("padding_x", 34 if typ=="situation_label" else (24 if typ=="end_message" else 46)))
    padding_y=int(item.get("padding_y", 20 if typ=="situation_label" else (18 if typ=="end_message" else 32)))
    scratch=Image.new("RGBA", (width, 1000), (0,0,0,0))
    d=ImageDraw.Draw(scratch)
    lines=wrap_text(d, item.get("text",""), font, max(1,width-2*padding_x))
    spacing=int(item.get("line_spacing", max(8, int(size*0.22))))
    bboxes=[d.textbbox((0,0), line or " ", font=font) for line in lines]
    line_heights=[b[3]-b[1] for b in bboxes]
    text_h=sum(line_heights)+spacing*max(0,len(lines)-1)
    return typ,size,font,padding_x,padding_y,lines,spacing,bboxes,line_heights,text_h


def _organic_cloud_layer(width: int, height: int, typ: str):
    """Deterministic, softly irregular Mongi dialogue/thought bubble.

    Built from overlapping lobes instead of a geometric rounded rectangle.
    No stroke is drawn. A lightly blurred alpha edge lets the ivory bubble blend
    into the illustration while remaining readable.
    """
    scale = 3
    W, H = width * scale, height * scale
    mask = Image.new("L", (W, H), 0)
    md = ImageDraw.Draw(mask)

    # Main soft body. Insets leave room for the irregular outer lobes.
    ix, iy = int(W * 0.055), int(H * 0.10)
    md.ellipse((ix, iy, W - ix, H - iy), fill=238)

    # Fixed asymmetric lobes: intentionally organic but deterministic so cache
    # and rerenders remain pixel-stable. Thought is slightly rounder/airier.
    lobes = [
        (0.04,0.22,0.24,0.62), (0.12,0.05,0.36,0.38),
        (0.31,0.01,0.55,0.30), (0.52,0.04,0.76,0.31),
        (0.72,0.12,0.96,0.48), (0.76,0.43,0.99,0.79),
        (0.58,0.69,0.84,0.98), (0.34,0.73,0.60,0.99),
        (0.12,0.66,0.39,0.96), (0.01,0.45,0.22,0.82),
    ]
    if typ == "thought":
        lobes += [(0.22,0.00,0.45,0.27), (0.64,0.02,0.87,0.34)]
    for x1,y1,x2,y2 in lobes:
        md.ellipse((int(W*x1),int(H*y1),int(W*x2),int(H*y2)), fill=238)

    # Feather only the edge; supersampling keeps the silhouette smooth.
    mask = mask.filter(ImageFilter.GaussianBlur(radius=max(2, int(scale*1.8))))
    mask = mask.resize((width, height), Image.Resampling.LANCZOS)
    alpha = mask.point(lambda a: int(a * 0.90))
    fill = (255, 250, 241) if typ == "dialogue" else (252, 249, 242)
    layer = Image.new("RGBA", (width, height), (*fill, 0))
    layer.putalpha(alpha)
    return layer


def render_text_overlay(item: dict, canvas_w: int, canvas_h: int, out_path: Path):
    typ=item.get("type","dialogue")
    width=int(item.get("width") or (260 if typ=="situation_label" else (900 if typ=="end_message" else 700)))
    typ,size,font,padding_x,padding_y,lines,spacing,bboxes,line_heights,text_h=_layout(item,width)
    height=int(item.get("height") or text_h+2*padding_y)
    img=Image.new("RGBA", (width,height), (0,0,0,0))
    d=ImageDraw.Draw(img)

    # End Card message is a dedicated text role: text only, generous negative
    # space, no dialogue/thought bubble or border. The End Card artwork itself
    # carries the fixed visual frame.
    if typ in {"dialogue", "thought"}:
        # Mongi Soft Bubble V1: irregular cloud silhouette, warm translucent
        # ivory, feathered edge, and deliberately NO dark outline.
        img.alpha_composite(_organic_cloud_layer(width, height, typ))
        d=ImageDraw.Draw(img)
    elif typ != "end_message":
        # Non-character UI/situation labels keep their existing UI treatment.
        radius=int(item.get("radius", height//2 if typ=="situation_label" else 34))
        bg=LABEL_BG if typ=="situation_label" else CREAM
        d.rounded_rectangle((1,1,width-2,height-2), radius=radius, fill=bg, outline=(126,96,74,180), width=2)

    # True visual vertical centering: account for glyph bbox top/bottom rather than
    # drawing from a fixed padding baseline. This fixes Korean text sitting low.
    y_cursor=max(0,(height-text_h)/2)
    align=str(item.get("align","center")).lower()
    for line,bbox,h in zip(lines,bboxes,line_heights):
        tw=bbox[2]-bbox[0]
        if align=="left":
            x=padding_x-bbox[0]
        elif align=="right":
            x=width-padding_x-tw-bbox[0]
        else:
            x=(width-tw)/2-bbox[0]
        # bbox[1] is the offset from drawing origin to visible glyph top.
        # Subtracting it centers the visible glyph, not the font baseline box.
        y=y_cursor-bbox[1]
        d.text((round(x),round(y)), line, font=font, fill=WARM_BROWN)
        y_cursor+=h+spacing
    out_path.parent.mkdir(parents=True, exist_ok=True)
    img.save(out_path)
    return width,height


def semantic_position(item, overlay_w, overlay_h, canvas_w, canvas_h):
    if item.get("x") is not None and item.get("y") is not None:
        return int(item["x"]), int(item["y"])
    if item.get("type") == "end_message" and item.get("position") is None:
        return (canvas_w-overlay_w)//2, int(canvas_h*0.28 - overlay_h/2)
    pos=item.get("position","ABOVE_CHARACTER")
    margin=70
    if pos=="TOP_LEFT": return margin, 130
    if pos=="TOP_RIGHT": return canvas_w-overlay_w-margin, 130
    if pos=="BOTTOM_LEFT": return margin, canvas_h-overlay_h-180
    if pos=="BOTTOM_RIGHT": return canvas_w-overlay_w-margin, canvas_h-overlay_h-180
    if pos=="CENTER": return (canvas_w-overlay_w)//2,(canvas_h-overlay_h)//2
    return (canvas_w-overlay_w)//2, 180
