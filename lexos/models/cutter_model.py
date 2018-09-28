"""This is the model that cuts files into segments."""

from typing import NamedTuple, Optional, Dict, List
from lexos.models.base_model import BaseModel
from lexos.models.filemanager_model import FileManagerModel
from lexos.receivers.cutter_receiver import CutterReceiver, \
    CutterFrontEndOptions


class File(NamedTuple):
    """Structure for each file."""

    label: str
    content: str


class CutterTestOptions(NamedTuple):
    """Cutter test front end options."""

    active_file_ids: List[int]
    file_id_label_map: Dict[int, str]
    file_id_content_map: Dict[int, str]
    cutter_front_end_option: CutterFrontEndOptions


class CutterModel(BaseModel):
    """This is the model for the cutter."""

    def __init__(self, test_option: Optional[CutterTestOptions] = None):
        """Initialize the class based on if test option was passed in.

        :param test_option: the options to send in for testing.
        """
        super().__init__()
        if test_option is not None:
            self._test_active_file_ids = test_option.active_file_ids
            self._test_file_id_label_map = test_option.file_id_label_map
            self._test_file_id_content_map = test_option.file_id_content_map
            self._test_front_end_options = test_option.cutter_front_end_option
        else:
            self._test_active_file_ids = None
            self._test_file_id_label_map = None
            self._test_file_id_content_map = None
            self._test_front_end_options = None

    @property
    def _cutter_option(self) -> CutterFrontEndOptions:
        """:return: cutter front end option."""
        return self._test_front_end_options \
            if self._test_front_end_options is not None \
            else CutterReceiver().options_from_front_end()

    @property
    def _active_file_ids(self) -> List[int]:
        """:return: list of ids of active files."""
        return self._test_active_file_ids \
            if self._test_active_file_ids is not None \
            else self._cutter_option.active_file_ids

    @property
    def _id_passages_map(self) -> Dict[int, str]:
        """Get a dictionary of file ids and file contents.

        :return: a dictionary where ids are keys and contents are items.
        """
        return self._test_file_id_content_map \
            if self._test_file_id_content_map is not None \
            else FileManagerModel().load_file_manager().\
            get_content_of_active_with_id()

    @property
    def _id_labels_map(self) -> Dict[int, str]:
        """Get a dictionary of file ids and file labels.

        :return: a dictionary where ids are keys and labels are items.
        """
        return self._test_file_id_label_map \
            if self._test_file_id_label_map is not None \
            else FileManagerModel().load_file_manager().\
            get_active_labels_with_id()

    @property
    def _active_file_label_content_map(self) -> List[File]:
        """:return: a list of File objects for the active files."""
        return [
            File(
                label=self._id_labels_map[active_id],
                content=self._id_passages_map[active_id]
            )
            for active_id in self._active_file_ids
        ]
