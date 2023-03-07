from random import randint

from lxml import etree
from xml2rfc.uniscripts import which_scripts
from xml2rfc.util.fonts import get_noto_serif_family_for_script


DRAFT_HEAD = """<?xml version="1.0" encoding="utf-8"?>

<rfc ipr="trust200902" docName="draft-rathnayake-xml2rfc-unicode-00" category="exp" submissionType="independent" tocInclude="true" sortRefs="true" symRefs="true">
  <front>
    <title abbrev="xml2rfc-unicode">Experiment with Unicode characters in xml2rfc</title>
    <author initials="K." surname="Nanayakkara Rathnayake" asciiFullname="Kesara Nanayakkara Rathnayake" fullname="&#3482;&#3545;&#3523;&#3515; &#3505;&#3535;&#3505;&#3535;&#3514;&#3482;&#3530;&#3482;&#3535;&#3515; &#3515;&#3501;&#3530;&#3505;&#3535;&#3514;&#3482;">
      <organization>IETF Administration LLC</organization>
      <address>
        <postal>
          <country>New Zealand</country>
        </postal>
        <email>kesara@fq.nz</email>
      </address>
    </author>
    <date year="2023" month="March" day="07"/>
    <abstract>
      <t>This draft is an experiment to explore what happens when various Unicode characters are on an Internet-Draft and how xml2rfc handles that.</t>
    </abstract>
  </front>
  <middle>
    <section anchor="introduction">
      <name>Introduction</name>
      <t>Non-ASCII characters are allowed in RFCs under several restrictions. See <xref target="RFC7997" />.</t>
      <t>Some XML2RFC elements allow the use of bare Unicode and other elements can make use of <tt>&gt;u&lt;</tt> element. See <xref target="RFC7991" />.</t>
      <t>Various non-Latin Unicode characters can be an issue in RFC publications. Especially generating PDF format of the document. This is because the correct font has to be identified and included in the PDF file. This is done by the xml2rfc too. See <xref target="xml2rfc" />.</t>
      <t>xml2rfc maintains its own list of Unicode script blocks. Depending on which script is used, xml2rfc matches the correct Noto font.</t>
      <t>This document is an experiment on when Unicode characters from different blocks are included in an Internet-Draft.</t>
    </section>
    <section>
      <name>Methodology</name>
      <t>The Unicode characters blocks are identified using <xref target="unicode-blocks" />.</t>
      <t>This random printable character from each block is chosen. The xml2rfc is used as an API to identify which script blocks are assigned to that character and predicted font names. xml2rfc might predict a non-existing font. These are the instances where xml2rfc might leak non-standard fonts to generated PDF files.</t>
    </section>
    <section>
      <name>Unicode code blocks</name>
    """


DRAFT_TAIL = """    </section>
  </middle>
  <back>
    <references>
      <name>Informative References</name>
      <reference anchor="RFC7997" target="https://www.rfc-editor.org/info/rfc7997">
        <front>
          <title>The Use of Non-ASCII Characters in RFCs</title>
          <author fullname="H. Flanagan" initials="H." role="editor" surname="Flanagan"/>
          <date month="December" year="2016"/>
          <abstract>
            <t>
              In order to support the internationalization of protocols and a more diverse Internet community, the RFC Series must evolve to allow for the use of non-ASCII characters in RFCs. While English remains the required language of the Series, the encoding of future RFCs will be in UTF-8, allowing for a broader range of characters than typically used in the English language. This document describes the RFC Editor requirements and gives guidance regarding the use of non-ASCII characters in RFCs.
            </t>
            <t>
              This document updates RFC 7322. Please view this document in PDF form to see the full text.
            </t>
          </abstract>
        </front>
        <seriesInfo name="RFC" value="7997"/>
        <seriesInfo name="DOI" value="10.17487/RFC7997"/>
      </reference>
      <reference anchor="RFC7991" target="https://www.rfc-editor.org/info/rfc7991">
        <front>
          <title>The "xml2rfc" Version 3 Vocabulary</title>
          <author fullname="P. Hoffman" initials="P." surname="Hoffman"/>
          <date month="December" year="2016"/>
          <abstract>
            <t>
              This document defines the "xml2rfc" version 3 vocabulary: an XML-based language used for writing RFCs and Internet-Drafts. It is heavily derived from the version 2 vocabulary that is also under discussion. This document obsoletes the v2 grammar described in RFC 7749.
            </t>
          </abstract>
        </front>
        <seriesInfo name="RFC" value="7991"/>
        <seriesInfo name="DOI" value="10.17487/RFC7991"/>
      </reference>
      <reference anchor="xml2rfc" target="https://github.com/ietf-tools/xml2rfc/">
        <front>
          <title>xml2rfc</title>
          <author>
            <organization>IETF</organization>
          </author>
          <date month="March" day="8" year="2023"/>
        </front>
      </reference>
      <reference anchor="unicode-blocks" target="https://www.unicode.org/Public/14.0.0/ucd/Blocks.txt">
        <front>
          <title>Blocks-14.0.0</title>
          <author>
            <organization>Unicode, Inc.</organization>
          </author>
          <date month="January" day="1" year="2021"/>
        </front>
      </reference>
    </references>
  </back>
</rfc>"""

BLOCKS = {
    'Basic Latin': (0x0000, 0x007F),
    'Latin-1 Supplement': (0x0080, 0x00FF),
    'Latin Extended-A': (0x0100, 0x017F),
    'Latin Extended-B': (0x0180, 0x024F),
    'IPA Extensions': (0x0250, 0x02AF),
    'Spacing Modifier Letters': (0x02B0, 0x02FF),
    'Combining Diacritical Marks': (0x0300, 0x036F),
    'Greek and Coptic': (0x0370, 0x03FF),
    'Cyrillic': (0x0400, 0x04FF),
    'Cyrillic Supplement': (0x0500, 0x052F),
    'Armenian': (0x0530, 0x058F),
    'Hebrew': (0x0590, 0x05FF),
    'Arabic': (0x0600, 0x06FF),
    'Syriac': (0x0700, 0x074F),
    'Arabic Supplement': (0x0750, 0x077F),
    'Thaana': (0x0780, 0x07BF),
    'NKo': (0x07C0, 0x07FF),
    'Samaritan': (0x0800, 0x083F),
    'Mandaic': (0x0840, 0x085F),
    'Syriac Supplement': (0x0860, 0x086F),
    'Arabic Extended-A': (0x08A0, 0x08FF),
    'Devanagari': (0x0900, 0x097F),
    'Bengali': (0x0980, 0x09FF),
    'Gurmukhi': (0x0A00, 0x0A7F),
    'Gujarati': (0x0A80, 0x0AFF),
    'Oriya': (0x0B00, 0x0B7F),
    'Tamil': (0x0B80, 0x0BFF),
    'Telugu': (0x0C00, 0x0C7F),
    'Kannada': (0x0C80, 0x0CFF),
    'Malayalam': (0x0D00, 0x0D7F),
    'Sinhala': (0x0D80, 0x0DFF),
    'Thai': (0x0E00, 0x0E7F),
    'Lao': (0x0E80, 0x0EFF),
    'Tibetan': (0x0F00, 0x0FFF),
    'Myanmar': (0x1000, 0x109F),
    'Georgian': (0x10A0, 0x10FF),
    'Hangul Jamo': (0x1100, 0x11FF),
    'Ethiopic': (0x1200, 0x137F),
    'Ethiopic Supplement': (0x1380, 0x139F),
    'Cherokee': (0x13A0, 0x13FF),
    'Unified Canadian Aboriginal Syllabics': (0x1400, 0x167F),
    'Ogham': (0x1680, 0x169F),
    'Runic': (0x16A0, 0x16FF),
    'Tagalog': (0x1700, 0x171F),
    'Hanunoo': (0x1720, 0x173F),
    'Buhid': (0x1740, 0x175F),
    'Tagbanwa': (0x1760, 0x177F),
    'Khmer': (0x1780, 0x17FF),
    'Mongolian': (0x1800, 0x18AF),
    'Unified Canadian Aboriginal Syllabics Extended': (0x18B0, 0x18FF),
    'Limbu': (0x1900, 0x194F),
    'Tai Le': (0x1950, 0x197F),
    'New Tai Lue': (0x1980, 0x19DF),
    'Khmer Symbols': (0x19E0, 0x19FF),
    'Buginese': (0x1A00, 0x1A1F),
    'Tai Tham': (0x1A20, 0x1AAF),
    'Combining Diacritical Marks Extended': (0x1AB0, 0x1AFF),
    'Balinese': (0x1B00, 0x1B7F),
    'Sundanese': (0x1B80, 0x1BBF),
    'Batak': (0x1BC0, 0x1BFF),
    'Lepcha': (0x1C00, 0x1C4F),
    'Ol Chiki': (0x1C50, 0x1C7F),
    'Cyrillic Extended-C': (0x1C80, 0x1C8F),
    'Georgian Extended': (0x1C90, 0x1CBF),
    'Sundanese Supplement': (0x1CC0, 0x1CCF),
    'Vedic Extensions': (0x1CD0, 0x1CFF),
    'Phonetic Extensions': (0x1D00, 0x1D7F),
    'Phonetic Extensions Supplement': (0x1D80, 0x1DBF),
    'Combining Diacritical Marks Supplement': (0x1DC0, 0x1DFF),
    'Latin Extended Additional': (0x1E00, 0x1EFF),
    'Greek Extended': (0x1F00, 0x1FFF),
    'General Punctuation': (0x2000, 0x206F),
    'Superscripts and Subscripts': (0x2070, 0x209F),
    'Currency Symbols': (0x20A0, 0x20CF),
    'Combining Diacritical Marks for Symbols': (0x20D0, 0x20FF),
    'Letterlike Symbols': (0x2100, 0x214F),
    'Number Forms': (0x2150, 0x218F),
    'Arrows': (0x2190, 0x21FF),
    'Mathematical Operators': (0x2200, 0x22FF),
    'Miscellaneous Technical': (0x2300, 0x23FF),
    'Control Pictures': (0x2400, 0x243F),
    'Optical Character Recognition': (0x2440, 0x245F),
    'Enclosed Alphanumerics': (0x2460, 0x24FF),
    'Box Drawing': (0x2500, 0x257F),
    'Block Elements': (0x2580, 0x259F),
    'Geometric Shapes': (0x25A0, 0x25FF),
    'Miscellaneous Symbols': (0x2600, 0x26FF),
    'Dingbats': (0x2700, 0x27BF),
    'Miscellaneous Mathematical Symbols-A': (0x27C0, 0x27EF),
    'Supplemental Arrows-A': (0x27F0, 0x27FF),
    'Braille Patterns': (0x2800, 0x28FF),
    'Supplemental Arrows-B': (0x2900, 0x297F),
    'Miscellaneous Mathematical Symbols-B': (0x2980, 0x29FF),
    'Supplemental Mathematical Operators': (0x2A00, 0x2AFF),
    'Miscellaneous Symbols and Arrows': (0x2B00, 0x2BFF),
    'Glagolitic': (0x2C00, 0x2C5F),
    'Latin Extended-C': (0x2C60, 0x2C7F),
    'Coptic': (0x2C80, 0x2CFF),
    'Georgian Supplement': (0x2D00, 0x2D2F),
    'Tifinagh': (0x2D30, 0x2D7F),
    'Ethiopic Extended': (0x2D80, 0x2DDF),
    'Cyrillic Extended-A': (0x2DE0, 0x2DFF),
    'Supplemental Punctuation': (0x2E00, 0x2E7F),
    'CJK Radicals Supplement': (0x2E80, 0x2EFF),
    'Kangxi Radicals': (0x2F00, 0x2FDF),
    'Ideographic Description Characters': (0x2FF0, 0x2FFF),
    'CJK Symbols and Punctuation': (0x3000, 0x303F),
    'Hiragana': (0x3040, 0x309F),
    'Katakana': (0x30A0, 0x30FF),
    'Bopomofo': (0x3100, 0x312F),
    'Hangul Compatibility Jamo': (0x3130, 0x318F),
    'Kanbun': (0x3190, 0x319F),
    'Bopomofo Extended': (0x31A0, 0x31BF),
    'CJK Strokes': (0x31C0, 0x31EF),
    'Katakana Phonetic Extensions': (0x31F0, 0x31FF),
    'Enclosed CJK Letters and Months': (0x3200, 0x32FF),
    'CJK Compatibility': (0x3300, 0x33FF),
    'CJK Unified Ideographs Extension A': (0x3400, 0x4DBF),
    'Yijing Hexagram Symbols': (0x4DC0, 0x4DFF),
    'CJK Unified Ideographs': (0x4E00, 0x9FFF),
    'Yi Syllables': (0xA000, 0xA48F),
    'Yi Radicals': (0xA490, 0xA4CF),
    'Lisu': (0xA4D0, 0xA4FF),
    'Vai': (0xA500, 0xA63F),
    'Cyrillic Extended-B': (0xA640, 0xA69F),
    'Bamum': (0xA6A0, 0xA6FF),
    'Modifier Tone Letters': (0xA700, 0xA71F),
    'Latin Extended-D': (0xA720, 0xA7FF),
    'Syloti Nagri': (0xA800, 0xA82F),
    'Common Indic Number Forms': (0xA830, 0xA83F),
    'Phags-pa': (0xA840, 0xA87F),
    'Saurashtra': (0xA880, 0xA8DF),
    'Devanagari Extended': (0xA8E0, 0xA8FF),
    'Kayah Li': (0xA900, 0xA92F),
    'Rejang': (0xA930, 0xA95F),
    'Hangul Jamo Extended-A': (0xA960, 0xA97F),
    'Javanese': (0xA980, 0xA9DF),
    'Myanmar Extended-B': (0xA9E0, 0xA9FF),
    'Cham': (0xAA00, 0xAA5F),
    'Myanmar Extended-A': (0xAA60, 0xAA7F),
    'Tai Viet': (0xAA80, 0xAADF),
    'Meetei Mayek Extensions': (0xAAE0, 0xAAFF),
    'Ethiopic Extended-A': (0xAB00, 0xAB2F),
    'Latin Extended-E': (0xAB30, 0xAB6F),
    'Cherokee Supplement': (0xAB70, 0xABBF),
    'Meetei Mayek': (0xABC0, 0xABFF),
    'Hangul Syllables': (0xAC00, 0xD7AF),
    'Hangul Jamo Extended-B': (0xD7B0, 0xD7FF),
    'High Surrogates': (0xD800, 0xDB7F),
    'High Private Use Surrogates': (0xDB80, 0xDBFF),
    'Low Surrogates': (0xDC00, 0xDFFF),
    'Private Use Area': (0xE000, 0xF8FF),
    'CJK Compatibility Ideographs': (0xF900, 0xFAFF),
    'Alphabetic Presentation Forms': (0xFB00, 0xFB4F),
    'Arabic Presentation Forms-A': (0xFB50, 0xFDFF),
    'Variation Selectors': (0xFE00, 0xFE0F),
    'Vertical Forms': (0xFE10, 0xFE1F),
    'Combining Half Marks': (0xFE20, 0xFE2F),
    'CJK Compatibility Forms': (0xFE30, 0xFE4F),
    'Small Form Variants': (0xFE50, 0xFE6F),
    'Arabic Presentation Forms-B': (0xFE70, 0xFEFF),
    'Halfwidth and Fullwidth Forms': (0xFF00, 0xFFEF),
    'Specials': (0xFFF0, 0xFFFF),
    'Linear B Syllabary': (0x10000, 0x1007F),
    'Linear B Ideograms': (0x10080, 0x100FF),
    'Aegean Numbers': (0x10100, 0x1013F),
    'Ancient Greek Numbers': (0x10140, 0x1018F),
    'Ancient Symbols': (0x10190, 0x101CF),
    'Phaistos Disc': (0x101D0, 0x101FF),
    'Lycian': (0x10280, 0x1029F),
    'Carian': (0x102A0, 0x102DF),
    'Coptic Epact Numbers': (0x102E0, 0x102FF),
    'Old Italic': (0x10300, 0x1032F),
    'Gothic': (0x10330, 0x1034F),
    'Old Permic': (0x10350, 0x1037F),
    'Ugaritic': (0x10380, 0x1039F),
    'Old Persian': (0x103A0, 0x103DF),
    'Deseret': (0x10400, 0x1044F),
    'Shavian': (0x10450, 0x1047F),
    'Osmanya': (0x10480, 0x104AF),
    'Osage': (0x104B0, 0x104FF),
    'Elbasan': (0x10500, 0x1052F),
    'Caucasian Albanian': (0x10530, 0x1056F),
    'Linear A': (0x10600, 0x1077F),
    'Cypriot Syllabary': (0x10800, 0x1083F),
    'Imperial Aramaic': (0x10840, 0x1085F),
    'Palmyrene': (0x10860, 0x1087F),
    'Nabataean': (0x10880, 0x108AF),
    'Hatran': (0x108E0, 0x108FF),
    'Phoenician': (0x10900, 0x1091F),
    'Lydian': (0x10920, 0x1093F),
    'Meroitic Hieroglyphs': (0x10980, 0x1099F),
    'Meroitic Cursive': (0x109A0, 0x109FF),
    'Kharoshthi': (0x10A00, 0x10A5F),
    'Old South Arabian': (0x10A60, 0x10A7F),
    'Old North Arabian': (0x10A80, 0x10A9F),
    'Manichaean': (0x10AC0, 0x10AFF),
    'Avestan': (0x10B00, 0x10B3F),
    'Inscriptional Parthian': (0x10B40, 0x10B5F),
    'Inscriptional Pahlavi': (0x10B60, 0x10B7F),
    'Psalter Pahlavi': (0x10B80, 0x10BAF),
    'Old Turkic': (0x10C00, 0x10C4F),
    'Old Hungarian': (0x10C80, 0x10CFF),
    'Hanifi Rohingya': (0x10D00, 0x10D3F),
    'Rumi Numeral Symbols': (0x10E60, 0x10E7F),
    'Old Sogdian': (0x10F00, 0x10F2F),
    'Sogdian': (0x10F30, 0x10F6F),
    'Brahmi': (0x11000, 0x1107F),
    'Kaithi': (0x11080, 0x110CF),
    'Sora Sompeng': (0x110D0, 0x110FF),
    'Chakma': (0x11100, 0x1114F),
    'Mahajani': (0x11150, 0x1117F),
    'Sharada': (0x11180, 0x111DF),
    'Sinhala Archaic Numbers': (0x111E0, 0x111FF),
    'Khojki': (0x11200, 0x1124F),
    'Multani': (0x11280, 0x112AF),
    'Khudawadi': (0x112B0, 0x112FF),
    'Grantha': (0x11300, 0x1137F),
    'Newa': (0x11400, 0x1147F),
    'Tirhuta': (0x11480, 0x114DF),
    'Siddham': (0x11580, 0x115FF),
    'Modi': (0x11600, 0x1165F),
    'Mongolian Supplement': (0x11660, 0x1167F),
    'Takri': (0x11680, 0x116CF),
    'Ahom': (0x11700, 0x1173F),
    'Dogra': (0x11800, 0x1184F),
    'Warang Citi': (0x118A0, 0x118FF),
    'Zanabazar Square': (0x11A00, 0x11A4F),
    'Soyombo': (0x11A50, 0x11AAF),
    'Pau Cin Hau': (0x11AC0, 0x11AFF),
    'Bhaiksuki': (0x11C00, 0x11C6F),
    'Marchen': (0x11C70, 0x11CBF),
    'Masaram Gondi': (0x11D00, 0x11D5F),
    'Gunjala Gondi': (0x11D60, 0x11DAF),
    'Makasar': (0x11EE0, 0x11EFF),
    'Cuneiform': (0x12000, 0x123FF),
    'Cuneiform Numbers and Punctuation': (0x12400, 0x1247F),
    'Early Dynastic Cuneiform': (0x12480, 0x1254F),
    'Egyptian Hieroglyphs': (0x13000, 0x1342F),
    'Anatolian Hieroglyphs': (0x14400, 0x1467F),
    'Bamum Supplement': (0x16800, 0x16A3F),
    'Mro': (0x16A40, 0x16A6F),
    'Bassa Vah': (0x16AD0, 0x16AFF),
    'Pahawh Hmong': (0x16B00, 0x16B8F),
    'Medefaidrin': (0x16E40, 0x16E9F),
    'Miao': (0x16F00, 0x16F9F),
    'Ideographic Symbols and Punctuation': (0x16FE0, 0x16FFF),
    'Tangut': (0x17000, 0x187FF),
    'Tangut Components': (0x18800, 0x18AFF),
    'Kana Supplement': (0x1B000, 0x1B0FF),
    'Kana Extended-A': (0x1B100, 0x1B12F),
    'Nushu': (0x1B170, 0x1B2FF),
    'Duployan': (0x1BC00, 0x1BC9F),
    'Shorthand Format Controls': (0x1BCA0, 0x1BCAF),
    'Byzantine Musical Symbols': (0x1D000, 0x1D0FF),
    'Musical Symbols': (0x1D100, 0x1D1FF),
    'Ancient Greek Musical Notation': (0x1D200, 0x1D24F),
    'Mayan Numerals': (0x1D2E0, 0x1D2FF),
    'Tai Xuan Jing Symbols': (0x1D300, 0x1D35F),
    'Counting Rod Numerals': (0x1D360, 0x1D37F),
    'Mathematical Alphanumeric Symbols': (0x1D400, 0x1D7FF),
    'Sutton SignWriting': (0x1D800, 0x1DAAF),
    'Glagolitic Supplement': (0x1E000, 0x1E02F),
    'Mende Kikakui': (0x1E800, 0x1E8DF),
    'Adlam': (0x1E900, 0x1E95F),
    'Indic Siyaq Numbers': (0x1EC70, 0x1ECBF),
    'Arabic Mathematical Alphabetic Symbols': (0x1EE00, 0x1EEFF),
    'Mahjong Tiles': (0x1F000, 0x1F02F),
    'Domino Tiles': (0x1F030, 0x1F09F),
    'Playing Cards': (0x1F0A0, 0x1F0FF),
    'Enclosed Alphanumeric Supplement': (0x1F100, 0x1F1FF),
    'Enclosed Ideographic Supplement': (0x1F200, 0x1F2FF),
    'Miscellaneous Symbols and Pictographs': (0x1F300, 0x1F5FF),
    'Emoticons': (0x1F600, 0x1F64F),
    'Ornamental Dingbats': (0x1F650, 0x1F67F),
    'Transport and Map Symbols': (0x1F680, 0x1F6FF),
    'Alchemical Symbols': (0x1F700, 0x1F77F),
    'Geometric Shapes Extended': (0x1F780, 0x1F7FF),
    'Supplemental Arrows-C': (0x1F800, 0x1F8FF),
    'Supplemental Symbols and Pictographs': (0x1F900, 0x1F9FF),
    'Chess Symbols': (0x1FA00, 0x1FA6F),
    'CJK Unified Ideographs Extension B': (0x20000, 0x2A6DF),
    'CJK Unified Ideographs Extension C': (0x2A700, 0x2B73F),
    'CJK Unified Ideographs Extension D': (0x2B740, 0x2B81F),
    'CJK Unified Ideographs Extension E': (0x2B820, 0x2CEAF),
    'CJK Unified Ideographs Extension F': (0x2CEB0, 0x2EBEF),
    'CJK Compatibility Ideographs Supplement': (0x2F800, 0x2FA1F),
    'Tags': (0xE0000, 0xE007F),
    'Variation Selectors Supplement': (0xE0100, 0xE01EF),
    'Supplementary Private Use Area-A': (0xF0000, 0xFFFFF),
    'Supplementary Private Use Area-B': (0x100000, 0x10FFFF),
}


def get_random_char_int(start, stop, tries_remaining=5):
    try:
        random_int = randint(char_range[0]+1, char_range[1])
        xml = f"<u>&#x{hex(random_int)[2:].upper().zfill(4)};</u>"
        etree.fromstring(xml)
        return random_int
    except etree.XMLSyntaxError:
        if tries_remaining == 0:
            return random_int
        else:
            return get_random_char_int(start, stop, tries_remaining=tries_remaining-1)



print(DRAFT_HEAD)


for block_name, char_range in BLOCKS.items():
    print("      <section>")
    print(f"        <name>{block_name}</name>")
    random_int = get_random_char_int(char_range[0], char_range[1])
    random_char = chr(random_int)
    scripts = which_scripts(random_char)
    scripts_list = ", ".join(scripts)
    print(f"        <t>Unicode character range: {hex(char_range[0])[2:].upper().zfill(4)}..{hex(char_range[1])[2:].upper().zfill(4)}</t>")
    print(f'        <t><eref target="https://www.unicode.org/charts/PDF/U{hex(char_range[0])[2:].upper().zfill(4)}.pdf">Unicode {block_name} character list</eref></t>')
    print(f"        <t>Scripts list as identified by xml2rfc: {scripts_list}</t>")

    valid_fonts = [i for i in scripts if i != 'Unknown']
    if len(valid_fonts) > 0:
        print("        <t>Following fonts are available:</t>")
        print("        <ul>")
        for script in valid_fonts:
            font_family = get_noto_serif_family_for_script(script)
            print(f"          <li>{font_family}</li>")
        print("        </ul>")
        print(f"        <t>Example: <u>&#x{hex(random_int)[2:].upper().zfill(4)};</u></t>")
    else:
        print("        <t>There are no supported fonts.</t>")
    print("      </section>")


print(DRAFT_TAIL)
