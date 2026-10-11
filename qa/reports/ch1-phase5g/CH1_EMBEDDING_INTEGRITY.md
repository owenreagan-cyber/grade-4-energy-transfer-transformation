# Chapter 1 — Embedding / Package Integrity Report (Phase 5H)

Overall: **PASS**

| Check | Result | Detail |
|---|---|---|
| video media present | **PASS** | media parts: ['ppt/media/image1.png', 'ppt/media/image10.png', 'ppt/media/image11.png', 'ppt/media/image12.png', 'ppt/media/image13.png', 'ppt/media/image14.png', 'ppt/media/image15.png', 'ppt/media/image16.png', 'ppt/media/image17.png', 'ppt/media/image18.png', 'ppt/media/image19.png', 'ppt/media/image2.png', 'ppt/media/image20.png', 'ppt/media/image3.png', 'ppt/media/image4.png', 'ppt/media/image5.png', 'ppt/media/image6.png', 'ppt/media/image7.png', 'ppt/media/image8.png', 'ppt/media/image9.png', 'ppt/media/media1.mp4'] |
| content-type declares video/mp4 | **PASS** | mp4 default present |
| slide 25 relationship references video | **PASS** | <?xml version='1.0' encoding='UTF-8' standalone='yes'?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slideLayout" Target="../slideLayouts/slideLayout7.xml"/><Relationship Id="rId2" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image" Target="../media/image13.png"/><Relationship Id="rId3" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/notesSlide" Target="../notesSlides/notesSlide25.xml"/><Relationship Id="rId4" Type="http://schemas.microsoft.com/office/2007/relationships/media" Target="../media/media1.mp4"/><Relationship Id="rId5" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/video" Target="../media/media1.mp4"/><Relationship Id="rId6" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image" Target="../media/image20.png"/></Relationships> |
| slide 25 has videoFile element | **PASS** | videoFile present |
| poster frame image present | **PASS** | poster images: ['ppt/media/image1.png', 'ppt/media/image10.png', 'ppt/media/image11.png', 'ppt/media/image12.png', 'ppt/media/image13.png', 'ppt/media/image14.png', 'ppt/media/image15.png', 'ppt/media/image16.png', 'ppt/media/image17.png', 'ppt/media/image18.png', 'ppt/media/image19.png', 'ppt/media/image2.png', 'ppt/media/image20.png', 'ppt/media/image3.png', 'ppt/media/image4.png', 'ppt/media/image5.png', 'ppt/media/image6.png', 'ppt/media/image7.png', 'ppt/media/image8.png', 'ppt/media/image9.png'] |
| click-to-play timing node present | **PASS** | p:video timing present |
| embedded video non-trivial size | **PASS** | 21733498 bytes of video |
| embedded mp4 decodes (ffprobe) | **PASS** | {
    "format": {
        "duration": "276.688980",
        "size": "21733498"
    }
}
 |
| exactly one mp4 packaged | **PASS** | video parts: ['ppt/media/media1.mp4'] |
| candidate differs from baseline | **PASS** | v6 6ce671b94f18e16d… vs v4 1f85244f69ba8cb5… |
| poster frame referenced on slide 25 | **PASS** | blip/media in slide25 |

> Package-integrity PASS means the MP4 is genuinely inside the PPTX ZIP, referenced by slide 25 relationships, declared in content types, with a poster frame and click-to-play timing. It does NOT certify Microsoft PowerPoint playback (see playback report).
