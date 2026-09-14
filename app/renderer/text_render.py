from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
from .config import ASSETS_DIR, DEFAULT_FONT_SIZE

WARM_BROWN = (90, 64, 48, 255)
CREAM = (255, 250, 241, 244)
LABEL_BG = (239, 229, 211, 246)


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
    typ=item.get("type","caption")
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


def render_text_overlay(item: dict, canvas_w: int, canvas_h: int, out_path: Path):
    typ=item.get("type","caption")
    if typ in {"dialogue", "thought"}:
        raise ValueError(f"{typ} is image-baked in Edit Lock V1.9 and cannot be rendered as an overlay")
    width=int(item.get("width") or (260 if typ=="situation_label" else (900 if typ=="end_message" else 700)))
    typ,size,font,padding_x,padding_y,lines,spacing,bboxes,line_heights,text_h=_layout(item,width)
    height=int(item.get("height") or text_h+2*padding_y)
    img=Image.new("RGBA", (width,height), (0,0,0,0))
    d=ImageDraw.Draw(img)

    # End Card message is a dedicated text role: text only, generous negative
    # space, no dialogue/thought bubble or border. The End Card artwork itself
    # carries the fixed visual frame.
    if typ != "end_message":
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
