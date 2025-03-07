from collections.abc import Generator
from pathlib import Path

from aa_edit_data.archiver_data import ArchiverData, Header, Sample, Scalar, Vector
from aa_edit_data.generated import EPICSEvent_pb2


class ArchiverDataGenerated(ArchiverData):
    def __init__(
        self,
        samples: int = 100,
        pv_type: int = 6,
        year: int = 2024,
        start: int = 0,
        seconds_gap: int = 1,
        nano_gap: int = 0,
    ):
        self.header = Header()
        self.header.pvname = "generated_test_data"
        self.header.year = year
        self.header.type = pv_type  # type: ignore
        self.pv_type = self._get_pv_type()
        self.proto_class = self._get_proto_class()
        self.samples = samples
        self.start = start
        self.seconds_gap = seconds_gap
        self.nano_gap = nano_gap
        self.filepath = Path("dummy")

    def get_samples(self) -> Generator[Sample]:
        """Read a PB file that is structured in the Archiver Appliance format.
        Gathers the header and samples from this file and assigns them to
        self.header self.samples.

        Args:
            filepath (PathLike): Path to PB file.
        """
        time_gap = self.seconds_gap * 10**9 + self.nano_gap
        time = self.start * 10**9
        for i in range(self.samples):
            sample = self.proto_class()
            sample.secondsintoyear = time // 10**9
            sample.nano = time % 10**9
            if isinstance(sample, Scalar):
                sample = self.assign_sample_value(sample, i)
            else:
                sample = self.assign_sample_value(
                    sample, [(i * 5 + j) for j in range(5)]
                )
            time += time_gap
            yield sample

    def get_samples_bytes(self) -> Generator[bytes]:
        for sample in self.get_samples():
            yield self.serialize(sample)

    def assign_sample_value(self, sample: Sample, val: int | list[int]) -> Sample:
        """Generate an appropriate value for a sample based on it's pv type.

        Args:
            val (int): The original value.

        Returns:
            str | bytes | int: The value converted to an oppropriate type.
        """
        if isinstance(sample, Scalar):
            assert isinstance(val, int)
            if isinstance(sample, EPICSEvent_pb2.ScalarString):
                sample.val = str(val)
            elif isinstance(
                sample, EPICSEvent_pb2.ScalarByte | EPICSEvent_pb2.V4GenericBytes
            ):
                sample.val = val.to_bytes(2, byteorder="big")
            else:
                sample.val = val
        elif isinstance(sample, Vector):
            assert isinstance(val, list)
            if isinstance(sample, EPICSEvent_pb2.VectorString):
                sample.val.extend([str(i) for i in val])
            else:
                sample.val.extend(val)
        return sample
