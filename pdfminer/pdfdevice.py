# -*- coding: utf-8 -*-

import six

from .pdffont import PDFUnicodeNotDefined, PDFCIDFont, PDFSimpleFont

from . import utils

##  PDFDevice
##
class PDFDevice(object):

    def __init__(self, rsrcmgr):
        self.rsrcmgr = rsrcmgr
        self.ctm = None
        return

    def __repr__(self):
        return '<PDFDevice>'

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def close(self):
        return

    def set_ctm(self, ctm):
        self.ctm = ctm
        return

    def begin_tag(self, tag, props=None):
        return

    def end_tag(self):
        return

    def do_tag(self, tag, props=None):
        return

    def begin_page(self, page, ctm):
        return

    def end_page(self, page):
        return

    def begin_figure(self, name, bbox, matrix):
        return

    def end_figure(self, name):
        return

    def paint_path(self, graphicstate, stroke, fill, evenodd, path):
        return

    def render_image(self, name, stream):
        return

    def render_string(self, textstate, seq, ncs, graphicstate):
        return


##  PDFTextDevice
##
class PDFTextDevice(PDFDevice):

    def render_string(self, textstate, seq, ncs, graphicstate, tj_index=None):
        matrix = utils.mult_matrix(textstate.matrix, self.ctm)
        font = textstate.font
        fontsize = textstate.fontsize
        scaling = textstate.scaling * .01
        charspace = textstate.charspace * scaling
        wordspace = textstate.wordspace * scaling
        rise = textstate.rise
        if font.is_multibyte():
            wordspace = 0
        dxscale = .001 * fontsize * scaling

        is_cid = isinstance(font, PDFCIDFont)

        if font.is_vertical():
            textstate.linematrix = self.render_string_vertical(
                seq, matrix, textstate.linematrix, font, fontsize,
                scaling, charspace, wordspace, rise, dxscale, ncs, graphicstate,
                tj_index=tj_index, is_cid=is_cid)
        else:
            textstate.linematrix = self.render_string_horizontal(
                seq, matrix, textstate.linematrix, font, fontsize,
                scaling, charspace, wordspace, rise, dxscale, ncs, graphicstate,
                tj_index=tj_index, is_cid=is_cid)
        return

    def render_string_horizontal(self, seq, matrix, pos,
                                 font, fontsize, scaling, charspace, wordspace,
                                 rise, dxscale, ncs, graphicstate,
                                 tj_index=None, is_cid=False):
        (x, y) = pos

        needcharspace = False
        for ix, obj in enumerate(seq):
            if utils.isnumber(obj):
                x -= obj*dxscale
                needcharspace = True
            else:
                if len(obj) == 2*len(font.decode(obj)):
                    two_byte_glyph = True
                elif len(obj) == len(font.decode(obj)):
                    two_byte_glyph = False
                else:
                    raise Exception("Unhandled case for glyphs! Check implementation!")


                for g_ix, cid in enumerate(font.decode(obj)):
                    if two_byte_glyph:
                        g_ixs = [2*g_ix, (2*g_ix)+1]
                    else:
                        g_ixs = [g_ix]

                    if needcharspace:
                        x += charspace

                    x += self.render_char(utils.translate_matrix(matrix, (x, y)),
                                          font, fontsize, scaling, rise, cid,
                                          ncs, graphicstate,
                                          tj_index=tj_index, tj_pos=ix,
                                          glyph_ixs=g_ixs, is_cid=is_cid)

                    if cid == 32 and wordspace:
                        x += wordspace

                    needcharspace = True

        return (x, y)

    def render_string_vertical(self, seq, matrix, pos,
                               font, fontsize, scaling, charspace, wordspace,
                               rise, dxscale, ncs, graphicstate,
                               tj_index=None, is_cid=False):
        (x, y) = pos

        needcharspace = False
        for ix, obj in enumerate(seq):
            if utils.isnumber(obj):
                y -= obj*dxscale
                needcharspace = True
            else:
                if len(obj) == 2*len(font.decode(obj)):
                    two_byte_glyph = True
                elif len(obj) == len(font.decode(obj)):
                    two_byte_glyph = False
                else:
                    raise Exception("Unhandled case for glyphs! Check implementation!")
                    

                for g_ix, cid in enumerate(font.decode(obj)):
                    if two_byte_glyph:
                        g_ixs = [2*g_ix, (2*g_ix)+1]
                    else:
                        g_ixs = [g_ix]

                    if needcharspace:
                        y += charspace

                    y += self.render_char(utils.translate_matrix(matrix, (x, y)),
                                          font, fontsize, scaling, rise, cid,
                                          ncs, graphicstate,
                                          tj_index=tj_index, tj_pos=ix,
                                          glyph_ixs=g_ixs, is_cid=is_cid)

                    if cid == 32 and wordspace:
                        y += wordspace

                    needcharspace = True
        return (x, y)

    def render_char(self, matrix, font, fontsize, scaling, rise, cid, ncs, graphicstate,
                    tj_index=None, tj_pos=None, glyph_ixs=None, is_cid=False):
        return 0


##  TagExtractor
##
class TagExtractor(PDFDevice):

    def __init__(self, rsrcmgr, outfp, codec='utf-8'):
        PDFDevice.__init__(self, rsrcmgr)
        self.outfp = outfp
        self.codec = codec
        self.pageno = 0
        self._stack = []
        return

    def render_string(self, textstate, seq, ncs, graphicstate):
        font = textstate.font
        text = ''
        for obj in seq:
            if isinstance(obj, six.text_type):
                obj = utils.make_compat_bytes(obj)
            if not isinstance(obj, six.binary_type):
                continue
            chars = font.decode(obj)
            for cid in chars:
                try:
                    char = font.to_unichr(cid)
                    text += char
                except PDFUnicodeNotDefined:
                    print(chars)
                    pass
        self.outfp.write(utils.enc(text, self.codec))
        return

    def begin_page(self, page, ctm):
        output = '<page id="%s" bbox="%s" rotate="%d">' % (self.pageno, utils.bbox2str(page.mediabox), page.rotate)
        self.outfp.write(utils.make_compat_bytes(output))
        return

    def end_page(self, page):
        self.outfp.write(utils.make_compat_bytes('</page>\n'))
        self.pageno += 1
        return

    def begin_tag(self, tag, props=None):
        s = ''
        if isinstance(props, dict):
            s = ''.join(' %s="%s"' % (utils.enc(k), utils.enc(str(v))) for (k, v)
                        in sorted(six.iteritems(props)))
        out_s = '<%s%s>' % (utils.enc(tag.name), s)
        self.outfp.write(utils.make_compat_bytes(out_s))
        self._stack.append(tag)
        return

    def end_tag(self):
        assert self._stack, str(self.pageno)
        tag = self._stack.pop(-1)
        out_s = '</%s>' % utils.enc(tag.name)
        self.outfp.write(utils.make_compat_bytes(out_s))
        return

    def do_tag(self, tag, props=None):
        self.begin_tag(tag, props)
        self._stack.pop(-1)
        return
