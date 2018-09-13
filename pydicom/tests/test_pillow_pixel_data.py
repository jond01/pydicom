# Copyright 2008-2018 pydicom authors. See LICENSE file for details.

import os
import sys

import pytest

import pydicom
from pydicom.filereader import dcmread
from pydicom.data import get_testdata_files
from pydicom.tag import Tag

# Python 3.4 pytest does not have pytest.param?
have_pytest_param = hasattr(pytest, 'param')

try:
    from pydicom.pixel_data_handlers import numpy_handler
    HAVE_NP = numpy_handler.HAVE_NP
except ImportError:
    HAVE_NP = False
    numpy_handler = None

try:
    from pydicom.pixel_data_handlers import pillow_handler
    HAVE_PIL = pillow_handler.HAVE_PIL
    HAVE_JPEG = pillow_handler.HAVE_JPEG
    HAVE_JPEG2K = pillow_handler.HAVE_JPEG2K
    import numpy as np
except ImportError:
    pillow_handler = None
    HAVE_PIL = False
    HAVE_JPEG = False
    HAVE_JPEG2K = False


pillow_missing_message = ("pillow is not available "
                          "in this test environment")

TEST_PIL = HAVE_NP and HAVE_PIL
TEST_JPEG = TEST_PIL and HAVE_JPEG
TEST_JPEG2K = TEST_PIL and HAVE_JPEG2K

empty_number_tags_name = get_testdata_files(
    "reportsi_with_empty_number_tags.dcm")[0]
rtplan_name = get_testdata_files("rtplan.dcm")[0]
rtdose_name = get_testdata_files("rtdose.dcm")[0]
ct_name = get_testdata_files("CT_small.dcm")[0]
mr_name = get_testdata_files("MR_small.dcm")[0]
truncated_mr_name = get_testdata_files("MR_truncated.dcm")[0]
jpeg2000_name = get_testdata_files("JPEG2000.dcm")[0]
jpeg2000_lossless_name = get_testdata_files(
    "MR_small_jp2klossless.dcm")[0]
jpeg_ls_lossless_name = get_testdata_files(
    "MR_small_jpeg_ls_lossless.dcm")[0]
jpeg_lossy_name = get_testdata_files("JPEG-lossy.dcm")[0]
jpeg_lossless_name = get_testdata_files("JPEG-LL.dcm")[0]
deflate_name = get_testdata_files("image_dfl.dcm")[0]
rtstruct_name = get_testdata_files("rtstruct.dcm")[0]
priv_SQ_name = get_testdata_files("priv_SQ.dcm")[0]
nested_priv_SQ_name = get_testdata_files("nested_priv_SQ.dcm")[0]
meta_missing_tsyntax_name = get_testdata_files(
    "meta_missing_tsyntax.dcm")[0]
no_meta_group_length = get_testdata_files(
    "no_meta_group_length.dcm")[0]
gzip_name = get_testdata_files("zipMR.gz")[0]
color_px_name = get_testdata_files("color-px.dcm")[0]
color_pl_name = get_testdata_files("color-pl.dcm")[0]
explicit_vr_le_no_meta = get_testdata_files(
    "ExplVR_LitEndNoMeta.dcm")[0]
explicit_vr_be_no_meta = get_testdata_files(
    "ExplVR_BigEndNoMeta.dcm")[0]
emri_name = get_testdata_files("emri_small.dcm")[0]
emri_big_endian_name = get_testdata_files(
    "emri_small_big_endian.dcm")[0]
emri_jpeg_ls_lossless = get_testdata_files(
    "emri_small_jpeg_ls_lossless.dcm")[0]
emri_jpeg_2k_lossless = get_testdata_files(
    "emri_small_jpeg_2k_lossless.dcm")[0]
color_3d_jpeg_baseline = get_testdata_files(
    "color3d_jpeg_baseline.dcm")[0]
sc_rgb_jpeg_dcmtk_411_YBR_FULL_422 = get_testdata_files(
    "SC_rgb_dcmtk_+eb+cy+np.dcm")[0]
sc_rgb_jpeg_dcmtk_411_YBR_FULL = get_testdata_files(
    "SC_rgb_dcmtk_+eb+cy+n1.dcm")[0]
sc_rgb_jpeg_dcmtk_422_YBR_FULL = get_testdata_files(
    "SC_rgb_dcmtk_+eb+cy+n2.dcm")[0]
sc_rgb_jpeg_dcmtk_444_YBR_FULL = get_testdata_files(
    "SC_rgb_dcmtk_+eb+cy+s4.dcm")[0]
sc_rgb_jpeg_dcmtk_422_YBR_FULL_422 = get_testdata_files(
    "SC_rgb_dcmtk_+eb+cy+s2.dcm")[0]
sc_rgb_jpeg_dcmtk_RGB = get_testdata_files(
    "SC_rgb_dcmtk_+eb+cr.dcm")[0]
sc_rgb_jpeg2k_gdcm_KY = get_testdata_files(
    "SC_rgb_gdcm_KY.dcm")[0]
ground_truth_sc_rgb_jpeg2k_gdcm_KY_gdcm = get_testdata_files(
    "SC_rgb_gdcm2k_uncompressed.dcm")[0]


"""
These files were generated by running:
dcmdjpeg SC_rgb_dcmtk_+eb+cr.dcm SC_rgb_dcmtk_ebcr_dcmd.dcm
for each of the files
dcmdjpeg is the dcmtk decompress DICOM jpeg utility
"""

ground_truth_sc_rgb_jpeg_dcmtk_411_YBR_FULL_422 = get_testdata_files(
    "SC_rgb_dcmtk_ebcynp_dcmd.dcm")[0]
ground_truth_sc_rgb_jpeg_dcmtk_411_YBR_FULL = get_testdata_files(
    "SC_rgb_dcmtk_ebcyn1_dcmd.dcm")[0]
ground_truth_sc_rgb_jpeg_dcmtk_422_YBR_FULL = get_testdata_files(
    "SC_rgb_dcmtk_ebcyn2_dcmd.dcm")[0]
ground_truth_sc_rgb_jpeg_dcmtk_444_YBR_FULL = get_testdata_files(
    "SC_rgb_dcmtk_ebcys4_dcmd.dcm")[0]
ground_truth_sc_rgb_jpeg_dcmtk_422_YBR_FULL_422 = get_testdata_files(
    "SC_rgb_dcmtk_ebcys2_dcmd.dcm")[0]
ground_truth_sc_rgb_jpeg_dcmtk_RGB = get_testdata_files(
    "SC_rgb_dcmtk_ebcr_dcmd.dcm")[0]


dir_name = os.path.dirname(sys.argv[0])
save_dir = os.getcwd()


class Test_JPEGLS_no_pillow(object):
    """Tests for decoding JPEG LS if pillow pixel handler is missing."""
    def setup(self):
        """Setup the test datasets."""
        self.jpeg_ls_lossless = dcmread(jpeg_ls_lossless_name)
        self.emri_jpeg_ls_lossless = dcmread(emri_jpeg_ls_lossless)
        self.original_handlers = pydicom.config.pixel_data_handlers
        pydicom.config.pixel_data_handlers = [numpy_handler]

    def teardown(self):
        """Reset the pixel data handlers."""
        pydicom.config.pixel_data_handlers = self.original_handlers

    def test_JPEG_LS_PixelArray(self):
        """Test decoding JPEG LS with only numpy fails."""
        with pytest.raises(NotImplementedError):
            self.jpeg_ls_lossless.pixel_array

    def test_emri_JPEG_LS_PixelArray(self):
        """Test decoding JPEG LS with only numpy fails."""
        with pytest.raises(NotImplementedError):
            self.emri_jpeg_ls_lossless.pixel_array


class Test_JPEG2000Tests_no_pillow(object):
    """Tests for decoding JPEG2K if pillow pixel handler is missing."""
    def setup(self):
        """Setup the test datasets."""
        self.jpeg_2k = dcmread(jpeg2000_name)
        self.jpeg_2k_lossless = dcmread(jpeg2000_lossless_name)
        self.emri_jpeg_2k_lossless = dcmread(emri_jpeg_2k_lossless)
        self.sc_rgb_jpeg2k_gdcm_KY = dcmread(sc_rgb_jpeg2k_gdcm_KY)
        self.original_handlers = pydicom.config.pixel_data_handlers
        pydicom.config.pixel_data_handlers = [numpy_handler]

    def teardown(self):
        """Reset the pixel data handlers."""
        pydicom.config.pixel_data_handlers = self.original_handlers

    def testJPEG2000(self):
        """Test reading element values works OK without Pillow."""
        # XX also tests multiple-valued AT data element
        elem = self.jpeg_2k.FrameIncrementPointer
        assert [Tag(0x0054, 0x0010), Tag(0x0054, 0x0020)] == elem

        elem = self.jpeg_2k.DerivationCodeSequence[0].CodeMeaning
        assert 'Lossy Compression' == elem

    def testJPEG2000PixelArray(self):
        """Test decoding JPEG2K with only numpy fails."""
        with pytest.raises(NotImplementedError):
            self.jpeg_2k_lossless.pixel_array

    def test_emri_JPEG2000PixelArray(self):
        """Test decoding JPEG2K with only numpy fails."""
        with pytest.raises(NotImplementedError):
            self.emri_jpeg_2k_lossless.pixel_array

    def test_jpeg2000_lossy(self):
        """Test decoding JPEG2K with only numpy fails."""
        with pytest.raises(NotImplementedError):
            self.sc_rgb_jpeg2k_gdcm_KY.pixel_array


class Test_JPEGlossyTests_no_pillow(object):
    """Tests for decoding JPEG lossy if pillow pixel handler is missing."""
    def setup(self):
        """Setup the test datasets."""
        self.jpeg_lossy = dcmread(jpeg_lossy_name)
        self.color_3d_jpeg = dcmread(color_3d_jpeg_baseline)
        self.original_handlers = pydicom.config.pixel_data_handlers
        pydicom.config.pixel_data_handlers = [numpy_handler]

    def teardown(self):
        """Reset the pixel data handlers."""
        pydicom.config.pixel_data_handlers = self.original_handlers

    def testJPEGlossy(self):
        """Test reading element values works OK without Pillow."""
        elem = self.jpeg_lossy.DerivationCodeSequence[0].CodeMeaning
        assert 'Lossy Compression' == elem

    def testJPEGlossyPixelArray(self):
        """Test decoding JPEG lossy with only numpy fails."""
        with pytest.raises(NotImplementedError):
            self.jpeg_lossy.pixel_array

    def testJPEGBaselineColor3DPixelArray(self):
        """Test decoding JPEG lossy with only numpy fails."""
        with pytest.raises(NotImplementedError):
            self.color_3d_jpeg.pixel_array


class Test_JPEGlosslessTests_no_pillow(object):
    """Tests for decoding JPEG lossless if pillow pixel handler is missing."""
    def setup(self):
        """Setup the test datasets."""
        self.jpeg_lossless = dcmread(jpeg_lossless_name)
        self.original_handlers = pydicom.config.pixel_data_handlers
        pydicom.config.pixel_data_handlers = [numpy_handler]

    def teardown(self):
        """Reset the pixel data handlers."""
        pydicom.config.pixel_data_handlers = self.original_handlers

    def testJPEGlossless(self):
        """Test reading element values works OK without Pillow."""
        elem = self.jpeg_lossless.SourceImageSequence[0]
        elem = elem.PurposeOfReferenceCodeSequence[0].CodeMeaning
        assert 'Uncompressed predecessor' == elem

    def testJPEGlosslessPixelArray(self):
        """Test decoding JPEG lossless with only numpy fails."""
        with pytest.raises(NotImplementedError):
            self.jpeg_lossless.pixel_array


@pytest.mark.skipif(
    not TEST_PIL,
    reason=pillow_missing_message)
class Test_JPEG_LS_with_pillow(object):
    """Tests for decoding JPEG LS if pillow pixel handler is available."""
    def setup(self):
        """Setup the test datasets."""
        self.jpeg_ls_lossless = dcmread(jpeg_ls_lossless_name)
        self.emri_jpeg_ls_lossless = dcmread(emri_jpeg_ls_lossless)
        self.original_handlers = pydicom.config.pixel_data_handlers
        pydicom.config.pixel_data_handlers = [pillow_handler, numpy_handler]

    def teardown(self):
        """Reset the pixel data handlers."""
        pydicom.config.pixel_data_handlers = self.original_handlers

    def test_JPEG_LS_PixelArray(self):
        """Test decoding JPEG LS with pillow handler fails."""
        with pytest.raises(NotImplementedError):
            self.jpeg_ls_lossless.pixel_array

    def test_emri_JPEG_LS_PixelArray(self):
        """Test decoding JPEG LS with pillow handler fails."""
        with pytest.raises(NotImplementedError):
            self.emri_jpeg_ls_lossless.pixel_array


@pytest.mark.skipif(
    not TEST_JPEG2K,
    reason=pillow_missing_message)
class Test_JPEG2000Tests_with_pillow(object):
    """Test decoding JPEG2K if pillow JPEG2K plugin is available."""
    def setup(self):
        """Setup the test datasets."""
        self.jpeg_2k = dcmread(jpeg2000_name)
        self.jpeg_2k_lossless = dcmread(jpeg2000_lossless_name)
        self.mr_small = dcmread(mr_name)
        self.emri_jpeg_2k_lossless = dcmread(emri_jpeg_2k_lossless)
        self.emri_small = dcmread(emri_name)
        self.sc_rgb_jpeg2k_gdcm_KY = dcmread(sc_rgb_jpeg2k_gdcm_KY)
        self.ground_truth_sc_rgb_jpeg2k_gdcm_KY_gdcm = dcmread(
            ground_truth_sc_rgb_jpeg2k_gdcm_KY_gdcm)
        self.original_handlers = pydicom.config.pixel_data_handlers
        pydicom.config.pixel_data_handlers = [pillow_handler, numpy_handler]

    def teardown(self):
        """Reset the pixel data handlers."""
        pydicom.config.pixel_data_handlers = self.original_handlers

    def test_raises_if_endianess_not_set(self):
        self.jpeg_2k_lossless.is_little_endian = None
        with pytest.raises(ValueError):
            _ = self.jpeg_2k_lossless.pixel_array

    def testJPEG2000(self):
        """Test reading element values works OK with pillow pixel handler."""
        # XX also tests multiple-valued AT data element
        got = self.jpeg_2k.FrameIncrementPointer
        assert [Tag(0x0054, 0x0010), Tag(0x0054, 0x0020)] == got

        got = self.jpeg_2k.DerivationCodeSequence[0].CodeMeaning
        assert 'Lossy Compression' == got

    def testJPEG2000PixelArray(self):
        """Test decoding JPEG2K with pillow handler succeeds."""
        a = self.jpeg_2k_lossless.pixel_array
        b = self.mr_small.pixel_array
        assert np.array_equal(a, b)

    def test_emri_JPEG2000PixelArray(self):
        """Test decoding JPEG2K with pillow handler succeeds."""
        a = self.emri_jpeg_2k_lossless.pixel_array
        b = self.emri_small.pixel_array
        assert np.array_equal(a, b)

    def test_jpeg2000_lossy(self):
        """Test decoding JPEG2K lossy with pillow handler fails."""
        with pytest.raises(NotImplementedError):
            self.sc_rgb_jpeg2k_gdcm_KY.pixel_array


@pytest.mark.skipif(
    not TEST_JPEG,
    reason=pillow_missing_message)
class Test_JPEGlossyTests_with_pillow(object):
    """Test decoding JPEG if pillow JPEG plugin is available."""
    def setup(self):
        """Setup the test datasets."""
        self.jpeg_lossy = dcmread(jpeg_lossy_name)
        self.color_3d_jpeg = dcmread(color_3d_jpeg_baseline)
        self.original_handlers = pydicom.config.pixel_data_handlers
        pydicom.config.pixel_data_handlers = [pillow_handler, numpy_handler]

    def teardown(self):
        """Reset the pixel data handlers."""
        pydicom.config.pixel_data_handlers = self.original_handlers

    def testJPEGlossless_odd_data_size(self):
        """Test decoding JPEG with pillow handler succeeds."""
        test_file = get_testdata_files('SC_rgb_small_odd_jpeg.dcm')[0]
        ds = dcmread(test_file)
        pixel_data = ds.pixel_array
        assert pixel_data.nbytes == 27
        assert pixel_data.shape == (3, 3, 3)

    def testJPEGlossy(self):
        """Test reading element values works OK with pillow pixel handler."""
        got = self.jpeg_lossy.DerivationCodeSequence[0].CodeMeaning
        assert 'Lossy Compression' == got

    def testJPEGlossyPixelArray(self):
        """Test decoding JPEG lossy with pillow handler fails."""
        with pytest.raises(NotImplementedError):
            self.jpeg_lossy.pixel_array

    def testJPEGBaselineColor3DPixelArray(self):
        """Test decoding JPEG with pillow handler succeeds."""
        assert "YBR_FULL_422" == self.color_3d_jpeg.PhotometricInterpretation

        a = self.color_3d_jpeg.pixel_array
        assert (120, 480, 640, 3) == a.shape
        # this test points were manually identified in Osirix viewer
        assert (41, 41, 41) == tuple(a[3, 159, 290, :])
        assert (57, 57, 57) == tuple(a[3, 169, 290, :])

        assert "YBR_FULL_422" == self.color_3d_jpeg.PhotometricInterpretation


@pytest.fixture(scope="module")
def test_with_pillow():
    original_handlers = pydicom.config.pixel_data_handlers
    pydicom.config.pixel_data_handlers = [pillow_handler, numpy_handler]
    yield original_handlers
    pydicom.config.pixel_data_handlers = original_handlers


if have_pytest_param:
    test_ids = [
        "JPEG_RGB_RGB",
        "JPEG_RGB_411_AS_YBR_FULL",
        "JPEG_RGB_411_AS_YBR_FULL_422",
        "JPEG_RGB_422_AS_YBR_FULL",
        "JPEG_RGB_422_AS_YBR_FULL_422",
        "JPEG_RGB_444_AS_YBR_FULL", ]

    testdata = [
        (sc_rgb_jpeg_dcmtk_RGB, "RGB",
         [
             (255, 0, 0),
             (255, 128, 128),
             (0, 255, 0),
             (128, 255, 128),
             (0, 0, 255),
             (128, 128, 255),
             (0, 0, 0),
             (64, 64, 64),
             (192, 192, 192),
             (255, 255, 255),
         ], ground_truth_sc_rgb_jpeg_dcmtk_RGB),
        pytest.param(
            sc_rgb_jpeg_dcmtk_411_YBR_FULL,
            "YBR_FULL",
            [
                (253, 1, 0),
                (253, 128, 132),
                (0, 255, 5),
                (127, 255, 127),
                (1, 0, 254),
                (127, 128, 255),
                (0, 0, 0),
                (64, 64, 64),
                (192, 192, 192),
                (255, 255, 255),
            ],
            ground_truth_sc_rgb_jpeg_dcmtk_411_YBR_FULL,
            marks=pytest.mark.xfail(
                reason="Pillow does not support "
                "non default jpeg lossy colorspaces")),
        pytest.param(
            sc_rgb_jpeg_dcmtk_411_YBR_FULL_422,
            "YBR_FULL_422",
            [
                (253, 1, 0),
                (253, 128, 132),
                (0, 255, 5),
                (127, 255, 127),
                (1, 0, 254),
                (127, 128, 255),
                (0, 0, 0),
                (64, 64, 64),
                (192, 192, 192),
                (255, 255, 255),
            ],
            ground_truth_sc_rgb_jpeg_dcmtk_411_YBR_FULL_422,
            marks=pytest.mark.xfail(
                reason="Pillow does not support "
                "non default jpeg lossy colorspaces")),
        (sc_rgb_jpeg_dcmtk_422_YBR_FULL, "YBR_FULL",
         [
             (254, 0, 0),
             (255, 127, 127),
             (0, 255, 5),
             (129, 255, 129),
             (0, 0, 254),
             (128, 127, 255),
             (0, 0, 0),
             (64, 64, 64),
             (192, 192, 192),
             (255, 255, 255),
         ], ground_truth_sc_rgb_jpeg_dcmtk_422_YBR_FULL),
        (sc_rgb_jpeg_dcmtk_422_YBR_FULL_422, "YBR_FULL_422",
         [
             (254, 0, 0),
             (255, 127, 127),
             (0, 255, 5),
             (129, 255, 129),
             (0, 0, 254),
             (128, 127, 255),
             (0, 0, 0),
             (64, 64, 64),
             (192, 192, 192),
             (255, 255, 255),
         ], ground_truth_sc_rgb_jpeg_dcmtk_422_YBR_FULL_422),
        (sc_rgb_jpeg_dcmtk_444_YBR_FULL, "YBR_FULL",
         [
             (254, 0, 0),
             (255, 127, 127),
             (0, 255, 5),
             (129, 255, 129),
             (0, 0, 254),
             (128, 127, 255),
             (0, 0, 0),
             (64, 64, 64),
             (192, 192, 192),
             (255, 255, 255),
         ], ground_truth_sc_rgb_jpeg_dcmtk_444_YBR_FULL), ]
else:
    test_ids = [
        "JPEG_RGB_RGB",
        "JPEG_RGB_422_AS_YBR_FULL",
        "JPEG_RGB_422_AS_YBR_FULL_422",
        "JPEG_RGB_444_AS_YBR_FULL", ]

    testdata = [
        (sc_rgb_jpeg_dcmtk_RGB, "RGB",
         [
             (255, 0, 0),
             (255, 128, 128),
             (0, 255, 0),
             (128, 255, 128),
             (0, 0, 255),
             (128, 128, 255),
             (0, 0, 0),
             (64, 64, 64),
             (192, 192, 192),
             (255, 255, 255),
         ], ground_truth_sc_rgb_jpeg_dcmtk_RGB),
        (sc_rgb_jpeg_dcmtk_422_YBR_FULL, "YBR_FULL",
         [
             (254, 0, 0),
             (255, 127, 127),
             (0, 255, 5),
             (129, 255, 129),
             (0, 0, 254),
             (128, 127, 255),
             (0, 0, 0),
             (64, 64, 64),
             (192, 192, 192),
             (255, 255, 255),
         ], ground_truth_sc_rgb_jpeg_dcmtk_422_YBR_FULL),
        (sc_rgb_jpeg_dcmtk_422_YBR_FULL_422, "YBR_FULL_422",
         [
             (254, 0, 0),
             (255, 127, 127),
             (0, 255, 5),
             (129, 255, 129),
             (0, 0, 254),
             (128, 127, 255),
             (0, 0, 0),
             (64, 64, 64),
             (192, 192, 192),
             (255, 255, 255),
         ], ground_truth_sc_rgb_jpeg_dcmtk_422_YBR_FULL_422),
        (sc_rgb_jpeg_dcmtk_444_YBR_FULL, "YBR_FULL",
         [
             (254, 0, 0),
             (255, 127, 127),
             (0, 255, 5),
             (129, 255, 129),
             (0, 0, 254),
             (128, 127, 255),
             (0, 0, 0),
             (64, 64, 64),
             (192, 192, 192),
             (255, 255, 255),
         ], ground_truth_sc_rgb_jpeg_dcmtk_444_YBR_FULL), ]


@pytest.mark.skipif(
    not TEST_JPEG,
    reason=pillow_missing_message)
@pytest.mark.parametrize(
    "image,PhotometricInterpretation,results,ground_truth",
    testdata,
    ids=test_ids)
def test_PI_RGB(test_with_pillow,
                image,
                PhotometricInterpretation,
                results,
                ground_truth):
    t = dcmread(image)
    assert t.PhotometricInterpretation == PhotometricInterpretation
    a = t.pixel_array
    assert a.shape == (100, 100, 3)
    """
    This complete test never gave a different result than
    just the 10 point test below

    gt = dcmread(ground_truth)
    b = gt.pixel_array
    for x in range(100):
        for y in range(100):
            assert tuple(a[x, y]) == tuple(b[x, y])
    """
    # this test points are from the ImageComments tag
    assert tuple(a[5, 50, :]) == results[0]
    assert tuple(a[15, 50, :]) == results[1]
    assert tuple(a[25, 50, :]) == results[2]
    assert tuple(a[35, 50, :]) == results[3]
    assert tuple(a[45, 50, :]) == results[4]
    assert tuple(a[55, 50, :]) == results[5]
    assert tuple(a[65, 50, :]) == results[6]
    assert tuple(a[75, 50, :]) == results[7]
    assert tuple(a[85, 50, :]) == results[8]
    assert tuple(a[95, 50, :]) == results[9]
    assert t.PhotometricInterpretation == PhotometricInterpretation


@pytest.mark.skipif(
    not TEST_JPEG,
    reason=pillow_missing_message)
class Test_JPEGlosslessTests_with_pillow(object):
    """Test decoding JPEG lossless if pillow JPEG plugin is available."""
    def setup(self):
        """Setup the test datasets."""
        self.jpeg_lossless = dcmread(jpeg_lossless_name)
        self.original_handlers = pydicom.config.pixel_data_handlers
        pydicom.config.pixel_data_handlers = [pillow_handler, numpy_handler]

    def teardown(self):
        """Reset the pixel data handlers."""
        pydicom.config.pixel_data_handlers = self.original_handlers

    def testJPEGlossless(self):
        """Test reading element values works OK with pillow pixel handler."""
        got = self.jpeg_lossless.SourceImageSequence[0]
        got = got.PurposeOfReferenceCodeSequence[0].CodeMeaning
        assert 'Uncompressed predecessor' == got

    def testJPEGlosslessPixelArray(self):
        """Test decoding JPEG lossless with pillow handler fails."""
        with pytest.raises(RuntimeError):
            self.jpeg_lossless.pixel_array
