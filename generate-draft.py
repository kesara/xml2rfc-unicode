from html import escape

from lxml import etree
from xml2rfc.uniscripts import which_scripts
from xml2rfc.util.fonts import get_noto_serif_family_for_script


DRAFT_HEAD = '''<?xml version="1.0" encoding="utf-8"?>

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
      <t>The Unicode characters blocks are identified using <xref target="blocks" />.</t>
      <t>The xml2rfc is used as an API to identify which script blocks are assigned to that character and predicted font names for set of characters from each Unicode code block. The xml2rfc might predict a non-existing font. These are the instances where xml2rfc might leak non-standard fonts to generated PDF files.</t>
    </section>'''


DRAFT_TAIL = '''
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
      <reference anchor="blocks" target="https://www.unicode.org/Public/15.0.0/ucd/Blocks.txt">
        <front>
          <title>Blocks-15.0.0</title>
          <author>
            <organization>Unicode, Inc.</organization>
          </author>
          <date month="January" day="28" year="2022"/>
        </front>
      </reference>
      <reference anchor="charts" target="https://www.unicode.org/charts/">
        <front>
          <title>Unicode 15.0 Character Code Charts</title>
          <author>
            <organization>Unicode, Inc.</organization>
          </author>
          <date month="March" day="8" year="2023"/>
        </front>
      </reference>
    </references>
  </back>
</rfc>'''

SCRIPTS_GROUPS = {'European Scripts': [{'Armenian': []}, {'Carian': []}, {'Caucasian Albanian': []}, {'Cypriot Syllabary': []}, {'Cypro-Minoan': []}, {'Cyrillic': []}, {'Cyrillic Supplement': []}, {'Cyrillic Extended-A': []}, {'Cyrillic Extended-B': []}, {'Cyrillic Extended-C': []}, {'Cyrillic Extended-D': []}, {'Elbasan': []}, {'Georgian': []}, {'Georgian Extended': []}, {'Georgian Supplement': []}, {'Glagolitic': []}, {'Glagolitic Supplement': []}, {'Gothic': []}, {'Greek and Coptic': []}, {'Greek Extended': []}, {'Ancient Greek Numbers': []}, {'Basic Latin': []}, {'Latin-1 Supplement': []}, {'Latin Extended-A': []}, {'Latin Extended-B': []}, {'Latin Extended-C': []}, {'Latin Extended-D': []}, {'Latin Extended-E': []}, {'Latin Extended-F': []}, {'Latin Extended-G': []}, {'Latin Extended Additional': []}, {'IPA Extensions': []}, {'Phonetic Extensions': []}, {'Phonetic Extensions Supplement': []}, {'Linear A': []}, {'Linear B': []}, {'Linear B Syllabary': []}, {'Linear B Ideograms': []}, {'Aegean Numbers': []}, {'Lycian': []}, {'Lydian': []}, {'Ogham': []}, {'Old Hungarian': []}, {'Old Italic': []}, {'Old Permic': []}, {'Phaistos Disc': []}, {'Runic': []}, {'Shavian': []}, {'Vithkuqi': []}], 'Modifier Letters': [{'Modifier Tone Letters': []}, {'Spacing Modifier Letters': []}, {'Superscripts and Subscripts': []}], 'Combining Marks': [{'Combining Diacritical Marks': []}, {'Combining Diacritical Marks Extended': []}, {'Combining Diacritical Marks Supplement': []}, {'Combining Diacritical Marks for Symbols': []}, {'Combining Half Marks': []}], 'Miscellaneous': [{'Alphabetic Presentation Forms': []}, {'Halfwidth and Fullwidth Forms': []}], 'African Scripts': [{'Adlam': []}, {'Bamum': []}, {'Bamum Supplement': []}, {'Bassa Vah': []}, {'Coptic': []}, {'Coptic Epact Numbers': []}, {'Egyptian Hieroglyphs': []}, {'Egyptian Hieroglyph Format Controls': []}, {'Ethiopic': []}, {'Ethiopic Supplement': []}, {'Ethiopic Extended': []}, {'Ethiopic Extended-A': []}, {'Ethiopic Extended-B': []}, {'Medefaidrin': []}, {'Mende Kikakui': []}, {'Meroitic': []}, {'Meroitic Cursive': []}, {'Meroitic Hieroglyphs': []}, {'NKo': []}, {'Osmanya': []}, {'Tifinagh': []}, {'Vai': []}], 'Middle Eastern Scripts': [{'Anatolian Hieroglyphs': []}, {'Arabic': []}, {'Arabic Supplement': []}, {'Arabic Extended-A': []}, {'Arabic Extended-B': []}, {'Arabic Extended-C': []}, {'Arabic Presentation Forms-A': []}, {'Arabic Presentation Forms-B': []}, {'Imperial Aramaic': []}, {'Avestan': []}, {'Chorasmian': []}, {'Cuneiform': []}, {'Cuneiform Numbers and Punctuation': []}, {'Early Dynastic Cuneiform': []}, {'Old Persian': []}, {'Ugaritic': []}, {'Elymaic': []}, {'Hatran': []}, {'Hebrew': ['Hebrew Presentation Forms']}, {'Mandaic': []}, {'Nabataean': []}, {'Old North Arabian': []}, {'Old South Arabian': []}, {'Inscriptional Pahlavi': []}, {'Psalter Pahlavi': []}, {'Palmyrene': []}, {'Inscriptional Parthian': []}, {'Phoenician': []}, {'Samaritan': []}, {'Syriac': ['Syriac Supplement']}, {'Yezidi': []}], 'Central Asian Scripts': [{'Manichaean': []}, {'Marchen': []}, {'Mongolian': []}, {'Mongolian Supplement': []}, {'Old Sogdian': []}, {'Old Turkic': []}, {'Old Uyghur': []}, {'Phags-pa': []}, {'Sogdian': []}, {'Soyombo': []}, {'Tibetan': []}, {'Zanabazar Square': []}], 'South Asian Scripts': [{'Ahom': []}, {'Bengali': []}, {'Bhaiksuki': []}, {'Brahmi': []}, {'Chakma': []}, {'Devanagari': []}, {'Devanagari Extended': []}, {'Devanagari Extended-A': []}, {'Dives Akuru': []}, {'Dogra': []}, {'Grantha': []}, {'Gujarati': []}, {'Gunjala Gondi': []}, {'Gurmukhi': []}, {'Kaithi': []}, {'Kannada': []}, {'Kharoshthi': []}, {'Khojki': []}, {'Khudawadi': []}, {'Lepcha': []}, {'Limbu': []}, {'Mahajani': []}, {'Malayalam': []}, {'Masaram Gondi': []}, {'Meetei Mayek': []}, {'Meetei Mayek Extensions': []}, {'Modi': []}, {'Mro': []}, {'Multani': []}, {'Nag Mundari': []}, {'Nandinagari': []}, {'Newa': []}, {'Ol Chiki': []}, {'Oriya': []}, {'Saurashtra': []}, {'Sharada': []}, {'Siddham': []}, {'Sinhala': []}, {'Sinhala Archaic Numbers': []}, {'Sora Sompeng': []}, {'Syloti Nagri': []}, {'Takri': []}, {'Tamil': []}, {'Tamil Supplement': []}, {'Telugu': []}, {'Thaana': []}, {'Tirhuta': []}, {'Toto': []}, {'Vedic Extensions': []}, {'Wancho': []}, {'Warang Citi': []}], 'Southeast Asian Scripts': [{'Cham': []}, {'Hanifi Rohingya': []}, {'Kayah Li': []}, {'Khmer': []}, {'Khmer Symbols': []}, {'Lao': []}, {'Myanmar': []}, {'Myanmar Extended-A': []}, {'Myanmar Extended-B': []}, {'New Tai Lue': []}, {'Nyiakeng Puachue Hmong': []}, {'Pahawh Hmong': []}, {'Pau Cin Hau': []}, {'Tai Le': []}, {'Tai Tham': []}, {'Tai Viet': []}, {'Tangsa': []}, {'Thai': []}], 'Indonesian & Philippine Scripts': [{'Balinese': []}, {'Batak': []}, {'Buginese': []}, {'Buhid': []}, {'Hanunoo': []}, {'Javanese': []}, {'Kawi': []}, {'Makasar': []}, {'Rejang': []}, {'Sundanese': []}, {'Sundanese Supplement': []}, {'Tagalog': []}, {'Tagbanwa': []}], 'East Asian Scripts': [{'Bopomofo': []}, {'Bopomofo Extended': []}, {'CJK Unified Ideographs': []}, {'CJK Unified Ideographs Extension A': []}, {'CJK Unified Ideographs Extension B': []}, {'CJK Unified Ideographs Extension C': []}, {'CJK Unified Ideographs Extension D': []}, {'CJK Unified Ideographs Extension E': []}, {'CJK Unified Ideographs Extension F': []}, {'CJK Unified Ideographs Extension G': []}, {'CJK Unified Ideographs Extension H': []}, {'CJK Compatibility Ideographs': []}, {'CJK Compatibility Ideographs Supplement': []}, {'Kangxi Radicals': []}, {'CJK Radicals Supplement': []}, {'CJK Strokes': []}, {'Ideographic Description Characters': []}, {'Hangul Jamo': []}, {'Hangul Jamo Extended-A': []}, {'Hangul Jamo Extended-B': []}, {'Hangul Compatibility Jamo': []}, {'Hangul Syllables': []}, {'Hiragana': []}, {'Kana Extended-A': []}, {'Kana Extended-B': []}, {'Kana Supplement': []}, {'Small Kana Extension': []}, {'Kanbun': []}, {'Katakana': []}, {'Katakana Phonetic Extensions': []}, {'Khitan Small Script': []}, {'Lisu': []}, {'Lisu Supplement': []}, {'Miao': []}, {'Nushu': []}, {'Tangut': []}, {'Tangut Components': []}, {'Tangut Supplement': []}, {'Yi': []}, {'Yi Syllables': []}, {'Yi Radicals': []}]}

SYMBOLS_GROUPS = {'Notational Systems': [{'Braille Patterns': []}, {'Musical Symbols': []}, {'Ancient Greek Musical Notation': []}, {'Byzantine Musical Symbols': []}, {'Znamenny Musical Notation': []}, {'Duployan': []}, {'Shorthand Format Controls': []}, {'Sutton SignWriting': []}], 'Punctuation': [{'General Punctuation': []}, {'Supplemental Punctuation': []}, {'CJK Symbols and Punctuation': []}, {'Ideographic Symbols and Punctuation': []}, {'CJK Compatibility Forms': []}, {'Halfwidth and Fullwidth Forms': []}, {'Small Form Variants': []}, {'Vertical Forms': []}], 'Alphanumeric Symbols': [{'Letterlike Symbols': []}, {'Mathematical Alphanumeric Symbols': []}, {'Arabic Mathematical Alphabetic Symbols': []}, {'Enclosed Alphanumerics': []}, {'Enclosed Alphanumeric Supplement': []}, {'Enclosed CJK Letters and Months': []}, {'Enclosed Ideographic Supplement': []}, {'CJK Compatibility': []}], 'Technical Symbols': [{'Control Pictures': []}, {'Miscellaneous Technical': []}, {'Optical Character Recognition': []}], 'Numbers & Digits': [{'Common Indic Number Forms': []}, {'Coptic Epact Numbers': []}, {'Counting Rod Numerals': []}, {'Cuneiform Numbers and Punctuation': []}, {'Indic Siyaq Numbers': []}, {'Kaktovik Numerals': []}, {'Mayan Numerals': []}, {'Number Forms': []}, {'Ottoman Siyaq Numbers': []}, {'Rumi Numeral Symbols': []}, {'Sinhala Archaic Numbers': []}, {'Superscripts and Subscripts': []}], 'Mathematical Symbols': [{'Arrows': []}, {'Supplemental Arrows-A': []}, {'Supplemental Arrows-B': []}, {'Supplemental Arrows-C': []}, {'Miscellaneous Symbols and Arrows': []}, {'Mathematical Alphanumeric Symbols': []}, {'Arabic Mathematical Alphabetic Symbols': []}, {'Letterlike Symbols': []}, {'Mathematical Operators': []}, {'Supplemental Mathematical Operators': []}, {'Miscellaneous Mathematical Symbols-A': []}, {'Miscellaneous Mathematical Symbols-B': []}, {'Geometric Shapes': []}, {'Box Drawing': []}, {'Block Elements': []}, {'Geometric Shapes Extended': []}], 'Emoji & Pictographs': [{'Dingbats': []}, {'Ornamental Dingbats': []}, {'Emoticons': []}, {'Miscellaneous Symbols': []}, {'Miscellaneous Symbols and Pictographs': []}, {'Supplemental Symbols and Pictographs': []}, {'Symbols and Pictographs Extended-A': []}, {'Transport and Map Symbols': []}], 'Other Symbols': [{'Alchemical Symbols': []}, {'Ancient Symbols': []}, {'Currency Symbols': []}, {'Game Symbols': []}, {'Chess Symbols': []}, {'Domino Tiles': []}, {'Mahjong Tiles': []}, {'Playing Cards': []}, {'Miscellaneous Symbols and Arrows': []}, {'Symbols for Legacy Computing': []}, {'Yijing Symbols': []}, {'Yijing Hexagram Symbols': []}, {'Tai Xuan Jing Symbols': []}], 'Specials': [{'Specials': []}, {'Tags': []}, {'Variation Selectors': []}, {'Variation Selectors Supplement': []}], 'Private Use': [{'Private Use Area': []}, {'Supplementary Private Use Area-A': []}, {'Supplementary Private Use Area-B': []}], 'Surrogates': [{'High Surrogates': []}, {'Low Surrogates': []}]}

BLOCKS = {'Basic Latin': (0, 127), 'Latin-1 Supplement': (128, 255), 'Latin Extended-A': (256, 383), 'Latin Extended-B': (384, 591), 'IPA Extensions': (592, 687), 'Spacing Modifier Letters': (688, 767), 'Combining Diacritical Marks': (768, 879), 'Greek and Coptic': (880, 1023), 'Cyrillic': (1024, 1279), 'Cyrillic Supplement': (1280, 1327), 'Armenian': (1328, 1423), 'Hebrew': (1424, 1535), 'Arabic': (1536, 1791), 'Syriac': (1792, 1871), 'Arabic Supplement': (1872, 1919), 'Thaana': (1920, 1983), 'NKo': (1984, 2047), 'Samaritan': (2048, 2111), 'Mandaic': (2112, 2143), 'Syriac Supplement': (2144, 2159), 'Arabic Extended-B': (2160, 2207), 'Arabic Extended-A': (2208, 2303), 'Devanagari': (2304, 2431), 'Bengali': (2432, 2559), 'Gurmukhi': (2560, 2687), 'Gujarati': (2688, 2815), 'Oriya': (2816, 2943), 'Tamil': (2944, 3071), 'Telugu': (3072, 3199), 'Kannada': (3200, 3327), 'Malayalam': (3328, 3455), 'Sinhala': (3456, 3583), 'Thai': (3584, 3711), 'Lao': (3712, 3839), 'Tibetan': (3840, 4095), 'Myanmar': (4096, 4255), 'Georgian': (4256, 4351), 'Hangul Jamo': (4352, 4607), 'Ethiopic': (4608, 4991), 'Ethiopic Supplement': (4992, 5023), 'Cherokee': (5024, 5119), 'Unified Canadian Aboriginal Syllabics': (5120, 5759), 'Ogham': (5760, 5791), 'Runic': (5792, 5887), 'Tagalog': (5888, 5919), 'Hanunoo': (5920, 5951), 'Buhid': (5952, 5983), 'Tagbanwa': (5984, 6015), 'Khmer': (6016, 6143), 'Mongolian': (6144, 6319), 'Unified Canadian Aboriginal Syllabics Extended': (6320, 6399), 'Limbu': (6400, 6479), 'Tai Le': (6480, 6527), 'New Tai Lue': (6528, 6623), 'Khmer Symbols': (6624, 6655), 'Buginese': (6656, 6687), 'Tai Tham': (6688, 6831), 'Combining Diacritical Marks Extended': (6832, 6911), 'Balinese': (6912, 7039), 'Sundanese': (7040, 7103), 'Batak': (7104, 7167), 'Lepcha': (7168, 7247), 'Ol Chiki': (7248, 7295), 'Cyrillic Extended-C': (7296, 7311), 'Georgian Extended': (7312, 7359), 'Sundanese Supplement': (7360, 7375), 'Vedic Extensions': (7376, 7423), 'Phonetic Extensions': (7424, 7551), 'Phonetic Extensions Supplement': (7552, 7615), 'Combining Diacritical Marks Supplement': (7616, 7679), 'Latin Extended Additional': (7680, 7935), 'Greek Extended': (7936, 8191), 'General Punctuation': (8192, 8303), 'Superscripts and Subscripts': (8304, 8351), 'Currency Symbols': (8352, 8399), 'Combining Diacritical Marks for Symbols': (8400, 8447), 'Letterlike Symbols': (8448, 8527), 'Number Forms': (8528, 8591), 'Arrows': (8592, 8703), 'Mathematical Operators': (8704, 8959), 'Miscellaneous Technical': (8960, 9215), 'Control Pictures': (9216, 9279), 'Optical Character Recognition': (9280, 9311), 'Enclosed Alphanumerics': (9312, 9471), 'Box Drawing': (9472, 9599), 'Block Elements': (9600, 9631), 'Geometric Shapes': (9632, 9727), 'Miscellaneous Symbols': (9728, 9983), 'Dingbats': (9984, 10175), 'Miscellaneous Mathematical Symbols-A': (10176, 10223), 'Supplemental Arrows-A': (10224, 10239), 'Braille Patterns': (10240, 10495), 'Supplemental Arrows-B': (10496, 10623), 'Miscellaneous Mathematical Symbols-B': (10624, 10751), 'Supplemental Mathematical Operators': (10752, 11007), 'Miscellaneous Symbols and Arrows': (11008, 11263), 'Glagolitic': (11264, 11359), 'Latin Extended-C': (11360, 11391), 'Coptic': (11392, 11519), 'Georgian Supplement': (11520, 11567), 'Tifinagh': (11568, 11647), 'Ethiopic Extended': (11648, 11743), 'Cyrillic Extended-A': (11744, 11775), 'Supplemental Punctuation': (11776, 11903), 'CJK Radicals Supplement': (11904, 12031), 'Kangxi Radicals': (12032, 12255), 'Ideographic Description Characters': (12272, 12287), 'CJK Symbols and Punctuation': (12288, 12351), 'Hiragana': (12352, 12447), 'Katakana': (12448, 12543), 'Bopomofo': (12544, 12591), 'Hangul Compatibility Jamo': (12592, 12687), 'Kanbun': (12688, 12703), 'Bopomofo Extended': (12704, 12735), 'CJK Strokes': (12736, 12783), 'Katakana Phonetic Extensions': (12784, 12799), 'Enclosed CJK Letters and Months': (12800, 13055), 'CJK Compatibility': (13056, 13311), 'CJK Unified Ideographs Extension A': (13312, 19903), 'Yijing Hexagram Symbols': (19904, 19967), 'CJK Unified Ideographs': (19968, 40959), 'Yi Syllables': (40960, 42127), 'Yi Radicals': (42128, 42191), 'Lisu': (42192, 42239), 'Vai': (42240, 42559), 'Cyrillic Extended-B': (42560, 42655), 'Bamum': (42656, 42751), 'Modifier Tone Letters': (42752, 42783), 'Latin Extended-D': (42784, 43007), 'Syloti Nagri': (43008, 43055), 'Common Indic Number Forms': (43056, 43071), 'Phags-pa': (43072, 43135), 'Saurashtra': (43136, 43231), 'Devanagari Extended': (43232, 43263), 'Kayah Li': (43264, 43311), 'Rejang': (43312, 43359), 'Hangul Jamo Extended-A': (43360, 43391), 'Javanese': (43392, 43487), 'Myanmar Extended-B': (43488, 43519), 'Cham': (43520, 43615), 'Myanmar Extended-A': (43616, 43647), 'Tai Viet': (43648, 43743), 'Meetei Mayek Extensions': (43744, 43775), 'Ethiopic Extended-A': (43776, 43823), 'Latin Extended-E': (43824, 43887), 'Cherokee Supplement': (43888, 43967), 'Meetei Mayek': (43968, 44031), 'Hangul Syllables': (44032, 55215), 'Hangul Jamo Extended-B': (55216, 55295), 'High Surrogates': (55296, 56191), 'High Private Use Surrogates': (56192, 56319), 'Low Surrogates': (56320, 57343), 'Private Use Area': (57344, 63743), 'CJK Compatibility Ideographs': (63744, 64255), 'Alphabetic Presentation Forms': (64256, 64335), 'Arabic Presentation Forms-A': (64336, 65023), 'Variation Selectors': (65024, 65039), 'Vertical Forms': (65040, 65055), 'Combining Half Marks': (65056, 65071), 'CJK Compatibility Forms': (65072, 65103), 'Small Form Variants': (65104, 65135), 'Arabic Presentation Forms-B': (65136, 65279), 'Halfwidth and Fullwidth Forms': (65280, 65519), 'Specials': (65520, 65535), 'Linear B Syllabary': (65536, 65663), 'Linear B Ideograms': (65664, 65791), 'Aegean Numbers': (65792, 65855), 'Ancient Greek Numbers': (65856, 65935), 'Ancient Symbols': (65936, 65999), 'Phaistos Disc': (66000, 66047), 'Lycian': (66176, 66207), 'Carian': (66208, 66271), 'Coptic Epact Numbers': (66272, 66303), 'Old Italic': (66304, 66351), 'Gothic': (66352, 66383), 'Old Permic': (66384, 66431), 'Ugaritic': (66432, 66463), 'Old Persian': (66464, 66527), 'Deseret': (66560, 66639), 'Shavian': (66640, 66687), 'Osmanya': (66688, 66735), 'Osage': (66736, 66815), 'Elbasan': (66816, 66863), 'Caucasian Albanian': (66864, 66927), 'Vithkuqi': (66928, 67007), 'Linear A': (67072, 67455), 'Latin Extended-F': (67456, 67519), 'Cypriot Syllabary': (67584, 67647), 'Imperial Aramaic': (67648, 67679), 'Palmyrene': (67680, 67711), 'Nabataean': (67712, 67759), 'Hatran': (67808, 67839), 'Phoenician': (67840, 67871), 'Lydian': (67872, 67903), 'Meroitic Hieroglyphs': (67968, 67999), 'Meroitic Cursive': (68000, 68095), 'Kharoshthi': (68096, 68191), 'Old South Arabian': (68192, 68223), 'Old North Arabian': (68224, 68255), 'Manichaean': (68288, 68351), 'Avestan': (68352, 68415), 'Inscriptional Parthian': (68416, 68447), 'Inscriptional Pahlavi': (68448, 68479), 'Psalter Pahlavi': (68480, 68527), 'Old Turkic': (68608, 68687), 'Old Hungarian': (68736, 68863), 'Hanifi Rohingya': (68864, 68927), 'Rumi Numeral Symbols': (69216, 69247), 'Yezidi': (69248, 69311), 'Arabic Extended-C': (69312, 69375), 'Old Sogdian': (69376, 69423), 'Sogdian': (69424, 69487), 'Old Uyghur': (69488, 69551), 'Chorasmian': (69552, 69599), 'Elymaic': (69600, 69631), 'Brahmi': (69632, 69759), 'Kaithi': (69760, 69839), 'Sora Sompeng': (69840, 69887), 'Chakma': (69888, 69967), 'Mahajani': (69968, 70015), 'Sharada': (70016, 70111), 'Sinhala Archaic Numbers': (70112, 70143), 'Khojki': (70144, 70223), 'Multani': (70272, 70319), 'Khudawadi': (70320, 70399), 'Grantha': (70400, 70527), 'Newa': (70656, 70783), 'Tirhuta': (70784, 70879), 'Siddham': (71040, 71167), 'Modi': (71168, 71263), 'Mongolian Supplement': (71264, 71295), 'Takri': (71296, 71375), 'Ahom': (71424, 71503), 'Dogra': (71680, 71759), 'Warang Citi': (71840, 71935), 'Dives Akuru': (71936, 72031), 'Nandinagari': (72096, 72191), 'Zanabazar Square': (72192, 72271), 'Soyombo': (72272, 72367), 'Unified Canadian Aboriginal Syllabics Extended-A': (72368, 72383), 'Pau Cin Hau': (72384, 72447), 'Devanagari Extended-A': (72448, 72543), 'Bhaiksuki': (72704, 72815), 'Marchen': (72816, 72895), 'Masaram Gondi': (72960, 73055), 'Gunjala Gondi': (73056, 73135), 'Makasar': (73440, 73471), 'Kawi': (73472, 73567), 'Lisu Supplement': (73648, 73663), 'Tamil Supplement': (73664, 73727), 'Cuneiform': (73728, 74751), 'Cuneiform Numbers and Punctuation': (74752, 74879), 'Early Dynastic Cuneiform': (74880, 75087), 'Cypro-Minoan': (77712, 77823), 'Egyptian Hieroglyphs': (77824, 78895), 'Egyptian Hieroglyph Format Controls': (78896, 78943), 'Anatolian Hieroglyphs': (82944, 83583), 'Bamum Supplement': (92160, 92735), 'Mro': (92736, 92783), 'Tangsa': (92784, 92879), 'Bassa Vah': (92880, 92927), 'Pahawh Hmong': (92928, 93071), 'Medefaidrin': (93760, 93855), 'Miao': (93952, 94111), 'Ideographic Symbols and Punctuation': (94176, 94207), 'Tangut': (94208, 100351), 'Tangut Components': (100352, 101119), 'Khitan Small Script': (101120, 101631), 'Tangut Supplement': (101632, 101759), 'Kana Extended-B': (110576, 110591), 'Kana Supplement': (110592, 110847), 'Kana Extended-A': (110848, 110895), 'Small Kana Extension': (110896, 110959), 'Nushu': (110960, 111359), 'Duployan': (113664, 113823), 'Shorthand Format Controls': (113824, 113839), 'Znamenny Musical Notation': (118528, 118735), 'Byzantine Musical Symbols': (118784, 119039), 'Musical Symbols': (119040, 119295), 'Ancient Greek Musical Notation': (119296, 119375), 'Kaktovik Numerals': (119488, 119519), 'Mayan Numerals': (119520, 119551), 'Tai Xuan Jing Symbols': (119552, 119647), 'Counting Rod Numerals': (119648, 119679), 'Mathematical Alphanumeric Symbols': (119808, 120831), 'Sutton SignWriting': (120832, 121519), 'Latin Extended-G': (122624, 122879), 'Glagolitic Supplement': (122880, 122927), 'Cyrillic Extended-D': (122928, 123023), 'Nyiakeng Puachue Hmong': (123136, 123215), 'Toto': (123536, 123583), 'Wancho': (123584, 123647), 'Nag Mundari': (124112, 124159), 'Ethiopic Extended-B': (124896, 124927), 'Mende Kikakui': (124928, 125151), 'Adlam': (125184, 125279), 'Indic Siyaq Numbers': (126064, 126143), 'Ottoman Siyaq Numbers': (126208, 126287), 'Arabic Mathematical Alphabetic Symbols': (126464, 126719), 'Mahjong Tiles': (126976, 127023), 'Domino Tiles': (127024, 127135), 'Playing Cards': (127136, 127231), 'Enclosed Alphanumeric Supplement': (127232, 127487), 'Enclosed Ideographic Supplement': (127488, 127743), 'Miscellaneous Symbols and Pictographs': (127744, 128511), 'Emoticons': (128512, 128591), 'Ornamental Dingbats': (128592, 128639), 'Transport and Map Symbols': (128640, 128767), 'Alchemical Symbols': (128768, 128895), 'Geometric Shapes Extended': (128896, 129023), 'Supplemental Arrows-C': (129024, 129279), 'Supplemental Symbols and Pictographs': (129280, 129535), 'Chess Symbols': (129536, 129647), 'Symbols and Pictographs Extended-A': (129648, 129791), 'Symbols for Legacy Computing': (129792, 130047), 'CJK Unified Ideographs Extension B': (131072, 173791), 'CJK Unified Ideographs Extension C': (173824, 177983), 'CJK Unified Ideographs Extension D': (177984, 178207), 'CJK Unified Ideographs Extension E': (178208, 183983), 'CJK Unified Ideographs Extension F': (183984, 191471), 'CJK Compatibility Ideographs Supplement': (194560, 195103), 'CJK Unified Ideographs Extension G': (196608, 201551), 'CJK Unified Ideographs Extension H': (201552, 205743), 'Tags': (917504, 917631), 'Variation Selectors Supplement': (917760, 917999), 'Supplementary Private Use Area-A': (983040, 1048575), 'Supplementary Private Use Area-B': (1048576, 1114111)}


def print_block(block_name, close=True):
    try:
        char_range = BLOCKS[block_name]
    except KeyError:
        print(f'<section><name>{block_name}</name>')
        if close:
            print('</section>')
        return

    print('<section>')
    print(f'<name>{block_name}</name>')
    print(f'<t>Unicode character range: U+{hex(char_range[0])[2:].upper().zfill(4)}..U+{hex(char_range[1])[2:].upper().zfill(4)}</t>')
    print(f'<t><eref target="https://www.unicode.org/charts/PDF/U{hex(char_range[0])[2:].upper().zfill(4)}.pdf">Unicode {block_name} character list</eref></t>')
    print(f'''
<table>
  <name>{block_name} Characters</name>
  <thead>
    <tr>
      <th>Character</th>
      <th>xml2rfc scripts</th>
      <th>xml2rfc fonts</th>
    </tr>
  </thead>
<tbody>''')
    for char_int in range(char_range[0], char_range[1])[:35]:
        print('<tr>')
        try:
            xml = f'<u>&#x{hex(char_int)[2:].upper().zfill(4)};</u>'
            etree.fromstring(xml)
            char = chr(char_int)
            scripts = which_scripts(char)
            scripts_list = ', '.join(scripts)
            fonts = ','.join(set([get_noto_serif_family_for_script(script) for script in scripts if script != 'Unknown']))
            print(f'<td>{xml}</td>')
            print(f'<td>{scripts_list}</td>')
            print(f'<td>{fonts}</td>')
        except etree.XMLSyntaxError:
            print(f'<td>{hex(char_int)[2:].upper().zfill(4)} is not supported</td>')
            print(f'<td></td>')
            print(f'<td></td>')
        print('</tr>')
    print('</tbody>')
    print('</table>')
    if close:
        print('</section>')


print(DRAFT_HEAD)

# Scripts section
print('''
<section>
  <name>Scripts</name>
  <t>This section covers Unicode scripts as defined in <xref target="charts" />.</t>''')
for script_group, scripts in SCRIPTS_GROUPS.items():
    print(f'<section><name>{escape(script_group)}</name>')
    for script_dict in scripts:
        for script, partial_scripts in script_dict.items():
            if len(partial_scripts) == 0:
                print_block(script)
            else:
                print_block(script, close=False)
                for partial_script in partial_scripts:
                    print_block(partial_script)
                print('</section>')
    print('</section>')
print('</section>')

# Symbols and Punctuation section
print('''
<section>
  <name>Symbols and Punctuation</name>
  <t>This section covers Unicode symbols and punctuation as defined in <xref target="charts" />.</t>''')
for script_group, scripts in SYMBOLS_GROUPS.items():
    print(f'<section><name>{escape(script_group)}</name>')
    for script_dict in scripts:
        for script, partial_scripts in script_dict.items():
            if len(partial_scripts) == 0:
                print_block(script)
            else:
                print_block(script, close=False)
                for partial_script in partial_scripts:
                    print_block(partial_script)
                print('</section>')
    print('</section>')
print('</section>')

print(DRAFT_TAIL)
