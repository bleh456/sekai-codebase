import logging
from fractions import Fraction

import PyNvVideoCodec as nvvc


class NVVCVideoDecoder:
    def __init__(self, enc_file, device_id, cuda_ctx, cuda_stream):
        """
        Create instance of HW-accelerated video decoder.
        :param enc_file: Full path to the MP4 file that needs to be decoded.
        :param device_id: id of video card which will be used for decoding & processing.
        :param cuda_ctx: A cuda context object.
        """
        self.device_id = device_id
        self.cuda_ctx = cuda_ctx
        self.enc_file = enc_file
        self.cuda_stream = cuda_stream
        # Demuxer is instantiated only to collect required information about
        # certain video file properties.
        self.nvDemux = nvvc.PyNvDemuxer(self.enc_file)
        self.nvDec = nvvc.CreateDecoder(
            gpuid=0,
            codec=self.nvDemux.GetNvCodecId(),
            cudacontext=self.cuda_ctx.handle,
            cudastream=self.cuda_stream.handle,
            usedevicememory=1,
        )

        self.width = self.nvDemux.Width()  # 1280
        self.height = self.nvDemux.Height()  # 720
        self.fps = self.nvDemux.FrameRate()  # 24
        self.pixelFormat = self.nvDec.GetPixelFormat()  # Pixel_Format.NV12

        self.frame_idx = 0

        logging.info(f"Width={self.width}, Height={self.height}, FrameRate={self.fps}, PixelFormat={self.pixelFormat}.")

    def __iter__(self):
        for packet in self.nvDemux:
            for frame in self.nvDec.Decode(packet):
                self.frame_idx += 1
                yield frame

    def finish(self):
        logging.info(f"Finish decode {self.frame_idx} frames.")


class NVVCVideoEncoder:
    def __init__(
        self,
        enc_file,
        device_id,
        width,
        height,
        fps,
        cuda_ctx,
        cuda_stream,
    ):
        self.device_id = device_id
        self.fps = round(Fraction(fps), 6)
        self.enc_file = enc_file
        self.cuda_ctx = cuda_ctx
        self.cuda_stream = cuda_stream

        self.nvEnc = nvvc.CreateEncoder(
            width,
            height,
            fmt="NV12",
            usecpuinutbuffer=0,
            codec="hevc",
            fps=fps,
            initqp="0,0,0",
            gop=240,
            tuning_info="high_quality",
            preset="P7",
            maxbitrate="4M",
            vbvinit="8M",
            vbvbufsize="8M",
            rc="vbr",
            temporalaq=1,
            aq=1,
            colorspace="bt709",
            cudastream=cuda_stream.handle,
        )

        self.frame_idx = 0

    def __call__(self, frame):
        bitstream = self.nvEnc.Encode(frame)  # List[int]
        self.frame_idx += 1

        bitstream = bytearray(bitstream)

        self.enc_file.write(bitstream)

    def finish(self):
        bitstream = self.nvEnc.EndEncode()

        if bitstream:
            bitstream = bytearray(bitstream)

            self.enc_file.write(bitstream)

        del self.nvEnc
