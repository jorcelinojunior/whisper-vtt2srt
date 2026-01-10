from whisper_vtt2srt.domain.models import SubtitleBlock, TimeCode


class TestTimeCode:
    def test_from_str_standard(self):
        # HH:MM:SS.mmm
        tc = TimeCode.from_str("01:02:03.456")
        assert tc.milliseconds == 3723456
        assert tc.to_srt_string() == "01:02:03,456"

    def test_from_str_short(self):
        # MM:SS.mmm
        tc = TimeCode.from_str("02:03.456")
        assert tc.milliseconds == 123456
        assert tc.to_srt_string() == "00:02:03,456"

    def test_from_str_no_millis(self):
        tc = TimeCode.from_str("00:00:01")
        assert tc.milliseconds == 1000

class TestSubtitleBlock:
    def test_duration_calculation(self):
        start = TimeCode(1000)
        end = TimeCode(1500)
        block = SubtitleBlock(index=1, start=start, end=end, lines=["Hello"])

        assert block.duration_ms == 500
