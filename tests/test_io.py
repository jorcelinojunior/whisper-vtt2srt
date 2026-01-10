from pathlib import Path

import pytest

from whisper_vtt2srt.use_cases.batch import BatchConverter


class TestBatchConverterIO:
    @pytest.fixture
    def sample_vtt(self):
        return """WEBVTT

00:00:01.000 --> 00:00:02.000
Hello
"""

    def test_single_file_conversion(self, tmp_path, sample_vtt):
        input_file = tmp_path / "test.vtt"
        input_file.write_text(sample_vtt, encoding="utf-8")

        converter = BatchConverter()
        results = converter.convert(str(input_file))

        assert len(results) == 1
        assert results[0] == str(tmp_path / "test.srt")
        assert (tmp_path / "test.srt").exists()

    def test_directory_conversion_flat(self, tmp_path, sample_vtt):
        # Create 2 VTT files
        (tmp_path / "a.vtt").write_text(sample_vtt)
        (tmp_path / "b.vtt").write_text(sample_vtt)
        # Create a non-VTT file
        (tmp_path / "c.txt").write_text("ignore me")

        converter = BatchConverter()
        results = converter.convert(str(tmp_path), recursive=False)

        assert len(results) == 2
        assert str(tmp_path / "a.srt") in results
        assert str(tmp_path / "b.srt") in results
        assert not (tmp_path / "c.srt").exists()

    def test_directory_conversion_recursive(self, tmp_path, sample_vtt):
        # layout:
        # /root.vtt
        # /sub/nested.vtt

        root_vtt = tmp_path / "root.vtt"
        root_vtt.write_text(sample_vtt)

        sub_dir = tmp_path / "sub"
        sub_dir.mkdir()
        nested_vtt = sub_dir / "nested.vtt"
        nested_vtt.write_text(sample_vtt)

        converter = BatchConverter()
        results = converter.convert(str(tmp_path), recursive=True)

        assert len(results) == 2
        assert str(tmp_path / "root.srt") in results
        assert str(sub_dir / "nested.srt") in results

    def test_encoding_support(self, tmp_path):
        # ISO-8859-1 content (Latin-1)
        # "Olá" encoded in latin-1 is b'Ol\xe1'
        content = "WEBVTT\n\n00:00:01.000 --> 00:00:02.000\nOlá"
        input_file = tmp_path / "latin.vtt"

        # Write with latin-1
        with open(input_file, "w", encoding="latin-1") as f:
            f.write(content)

        converter = BatchConverter()

        # Should fail with default utf-8
        with pytest.raises(UnicodeDecodeError):
            converter.convert(str(input_file), encoding="utf-8")

        # Should succeed with latin-1
        results = converter.convert(str(input_file), encoding="latin-1")
        assert len(results) == 1

        # Output is always UTF-8
        output_content = Path(results[0]).read_text(encoding="utf-8")
        assert "Olá" in output_content
