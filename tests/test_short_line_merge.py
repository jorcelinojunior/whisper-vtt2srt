
from whisper_vtt2srt.domain.models import SubtitleBlock, TimeCode
from whisper_vtt2srt.domain.options import CleaningOptions
from whisper_vtt2srt.use_cases.filters import ShortLineMerger


def create_block(lines: list, index=1):
    return SubtitleBlock(
        index=index,
        start=TimeCode(0),
        end=TimeCode(1000),
        lines=lines
    )

class TestShortLineMerger:
    def test_merge_short_lines_enabled(self):
        """Should merge lines when they fit within max_line_length."""
        options = CleaningOptions(merge_short_lines=True, max_line_length=20)
        filter_ = ShortLineMerger()

        # "Hello" (5) + " " (1) + "World" (5) = 11 <= 20
        block = create_block(["Hello", "World"])

        result = filter_.apply([block], options)

        assert len(result[0].lines) == 1
        assert result[0].lines[0] == "Hello World"

    def test_do_not_merge_if_exceeds_length(self):
        """Should NOT merge if combined length exceeds max_line_length."""
        options = CleaningOptions(merge_short_lines=True, max_line_length=10)
        filter_ = ShortLineMerger()

        # "Hello" (5) + " " (1) + "World" (5) = 11 > 10
        block = create_block(["Hello", "World"])

        result = filter_.apply([block], options)

        assert len(result[0].lines) == 2
        assert result[0].lines == ["Hello", "World"]

    def test_disabled_by_default(self):
        """Should do nothing if option is disabled."""
        options = CleaningOptions(merge_short_lines=False)
        filter_ = ShortLineMerger()

        block = create_block(["Hello", "World"])
        result = filter_.apply([block], options)

        assert result[0].lines == ["Hello", "World"]

    def test_progressive_merge(self):
        """Should merge strictly what fits, carrying over what doesn't."""
        # Max 15 chars
        options = CleaningOptions(merge_short_lines=True, max_line_length=15)
        filter_ = ShortLineMerger()

        # "A" (1)
        # "short" (5) -> "A short" (7) ... OK
        # "sentence" (8) -> "A short sentence" (16) ... FAIL (>15)
        # Result: ["A short", "sentence"]

        block = create_block(["A", "short", "sentence"])

        result = filter_.apply([block], options)

        assert result[0].lines == ["A short", "sentence"]
