import mne


class DatasetHandler:
    tmin: int = -1.0
    tmax: int = 4.0
    subject: int = 1
    runs: list = [6, 10, 14]  # motor imagery: hands vs feet
    event_id: dict = {"hands": 2, "feet": 3}

    montage = mne.channels.make_standard_montage("standard_1005")

    def _load_raw_data(self) -> mne.io.edf.edf.RawEDF:
        raw_fnames = mne.datasets.eegbci.load_data(self.subject, self.runs)
        return mne.io.concatenate_raws(
            [mne.io.read_raw_edf(f, preload=True) for f in raw_fnames]
        )

    def _preprocess_raw_data(self, raw_data: mne.io.edf.edf.RawEDF):
        # set channel names
        mne.datasets.eegbci.standardize(raw_data)
        raw_data.set_montage(self.montage)
        # strip channel names of "." characters
        raw_data.rename_channels(lambda x: x.strip("."))
        return raw_data

    def __init__(self):
        raw_data:mne.io.edf.edf.RawEDF = self._preprocess_raw_data(self._load_raw_data())
        # Apply band-pass filter
        raw_data.filter(7.0, 30.0, fir_design="firwin", skip_by_annotation="edge")
        events, _ = mne.events_from_annotations(raw_data, event_id=dict(T1=2, T2=3))
        picks = mne.pick_types(
            raw_data.info, meg=False, eeg=True, stim=False, eog=False, exclude="bads"
        )

        # Read epochs (train will be done only between 1 and 2s)
        # Testing will be done with a running classifier
        epochs = mne.Epochs(
            raw_data,
            events,
            self.event_id,
            self.tmin,
            self.tmax,
            proj=True,
            picks=picks,
            baseline=None,
            preload=True,
        )
        epochs_train = epochs.copy().crop(tmin=1.0, tmax=2.0)
        labels = epochs.events[:, -1] - 2
