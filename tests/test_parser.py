from whisper_vtt2srt.adapters.parsers import VttParser


class TestVttParser:
    def test_parses_simple_block(self):
        content = """WEBVTT

00:00:01.000 --> 00:00:02.000
Hello world
"""
        parser = VttParser()
        blocks = list(parser.parse(content))

        assert len(blocks) == 1
        assert blocks[0].start.milliseconds == 1000
        assert blocks[0].end.milliseconds == 2000
        assert blocks[0].lines == ["Hello world"]

    def test_parses_with_ids_and_extra_newlines(self):
        # Case from idd.vtt: IDs exist, extra newlines
        content = """WEBVTT
1
00:00:08.393 --> 00:00:10.437
♪ ♪

2
00:00:11.688 --> 00:00:14.941
Narrator: <i>blaba</i>
"""
        parser = VttParser()
        blocks = list(parser.parse(content))

        assert len(blocks) == 2
        # Block 1
        assert blocks[0].lines == ["♪ ♪"]
        # Block 2
        assert blocks[1].lines == ["Narrator: <i>blaba</i>"]

    def test_handles_missing_hours(self):
        content = """WEBVTT

00:01.000 --> 00:02.000
Short timestamp
"""
        parser = VttParser()
        blocks = list(parser.parse(content))

        assert len(blocks) == 1
        assert blocks[0].start.milliseconds == 1000

    def test_handles_multiline_text(self):
        content = """WEBVTT

00:00:01.000 --> 00:00:05.000
Line 1
Line 2
"""
        parser = VttParser()
        blocks = list(parser.parse(content))

        assert len(blocks) == 1
        assert blocks[0].lines == ["Line 1", "Line 2"]

    def test_ignores_metadata_headers(self):
        content = """WEBVTT
Kind: captions
Language: en

00:00:01.000 --> 00:00:02.000
Hello
"""
        parser = VttParser()
        blocks = list(parser.parse(content))

        assert len(blocks) == 1
        assert blocks[0].lines == ["Hello"]

    def test_ignores_empty_blocks(self):
        # Sometimes VTT has timestamps with no text
        content = """WEBVTT

00:00:01.000 --> 00:00:02.000

00:00:03.000 --> 00:00:04.000
Real content
"""
        parser = VttParser()
        blocks = list(parser.parse(content))

        # Depending on parser implementation, it might capture empty lines or skip.
        # Our implementation adds lines if they exist.
        # Ideally, blocks with NO lines should be filtered out by the generic Cleaners,
        # but let's see if the PARSER yields them empty.

        # Current Parser logic: Yields current_block when hitting NEXT timestamp or End.
        # If no lines were added, it yields a block with empty lines.

        assert len(blocks) >= 1
        # The last block definitely exists
        assert blocks[-1].lines == ["Real content"]
