import os.path

import fiftyone as fo
import fiftyone.utils.data as foud
import json


class COCOCustomLabeledImageDatasetImporter(foud.LabeledImageDatasetImporter):
    """Custom importer for labeled image datasets.

        Args:
            dataset_dir (None): the dataset directory. This may be optional for
                some importers
            shuffle (False): whether to randomly shuffle the order in which the
                samples are imported
            seed (None): a random seed to use when shuffling
            max_samples (None): a maximum number of samples to import. By default,
                all samples are imported
            **kwargs: additional keyword arguments for your importer
        """

    def __init__(
            self,
            dataset_dir=None,
            shuffle=False,
            seed=None,
            max_samples=None,
            **kwargs,
    ):
        super().__init__(
            dataset_dir=dataset_dir,
            shuffle=shuffle,
            seed=seed,
            max_samples=max_samples,
        )
        self._labels_file = None
        self._labels = None
        self._iter_labels = None
        self._max_samples = max_samples
        print("Hello")
        # self.next = 0
    def __iter__(self):
        # for label in self._labels:
            # print(label)
            # print("======================")
        self._iter_labels = iter(self._labels)
        return self

    def __len__(self):
        """The total number of samples that will be imported.

        Raises:
            TypeError: if the total number is not known
        """
        # Return the total number of samples in the dataset (if known)
        return len(self._labels)

    def __next__(self):
        """Returns information about the next sample in the dataset.

        Returns:
            an  ``(image_path, image_metadata, label)`` tuple, where

            -   ``image_path``: the path to the image on disk
            -   ``image_metadata``: an
                :class:`fiftyone.core.metadata.ImageMetadata` instances for the
                image, or ``None`` if :meth:`has_image_metadata` is ``False``
            -   ``label``: an instance of :meth:`label_cls`, or a dictionary
                mapping field names to :class:`fiftyone.core.labels.Label`
                instances, or ``None`` if the sample is unlabeled

        Raises:
            StopIteration: if there are no more samples to import
        """
        # Implement loading the next sample in your dataset here
        # print("hello next")
        (filepath,
         size_bytes,
         mime_type,
         width,
         height,
         num_channels,
         label,
         ) = next(self._iter_labels)

        image_metadata = fo.ImageMetadata(
            size_bytes = size_bytes,
            mime_type = mime_type,
            width = width,
            height = height,
            num_channels = num_channels,
        )
        label = fo.Classification(label = label)
        return filepath, image_metadata, label


    @property
    def has_dataset_info(self):
        """Whether this importer produces a dataset info dictionary."""
        # Return True or False here
        return False

    @property
    def has_image_metadata(self):
        """Whether this importer produces
        :class:`fiftyone.core.metadata.ImageMetadata` instances for each image.
        """
        # Return True or False here
        return True

    @property
    def label_cls(self):
        """The :class:`fiftyone.core.labels.Label` class(es) returned by this
        importer.

        This can be any of the following:

        -   a :class:`fiftyone.core.labels.Label` class. In this case, the
            importer is guaranteed to return labels of this type
        -   a list or tuple of :class:`fiftyone.core.labels.Label` classes. In
            this case, the importer can produce a single label field of any of
            these types
        -   a dict mapping keys to :class:`fiftyone.core.labels.Label` classes.
            In this case, the importer will return label dictionaries with keys
            and value-types specified by this dictionary. Not all keys need be
            present in the imported labels
        -   ``None``. In this case, the importer makes no guarantees about the
            labels that it may return
        """
        # Return the appropriate value here
        return {"class":fo.Classification, "segment":fo.Polylines}
        # return fo.Classification

    def setup(self):
        """Performs any necessary setup before importing the first sample in
        the dataset.

        This method is called when the importer's context manager interface is
        entered, :func:`DatasetImporter.__enter__`.
        """
        # Your custom setup here
        labels_path = os.path.join(self.dataset_dir, "Dataset/annotations", "annotations.json")
        labels = []
        with open(labels_path, "r") as f:
            reader = json.load(f)
            for item in reader:
                for annot in item["annotations"]:
                    l = ""
                    if annot is not None:
                        l = str(annot["category_id"])
                    labels.append((
                        os.path.join(self.dataset_dir, "Dataset/images", item["file_name"]),
                        "0",
                        "",
                        item["width"],
                        item["height"],
                        "3",
                        l,
                    ))
        self._labels = self._preprocess_list(labels)

    def get_dataset_info(self):
        """Returns the dataset info for the dataset.

        By convention, this method should be called after all samples in the
        dataset have been imported.

        Returns:
            a dict of dataset info
        """
        # Return a dict of dataset info, if supported by your importer
        pass

    def close(self, *args):
        """Performs any necessary actions after the last sample has been
        imported.

        This method is called when the importer's context manager interface is
        exited, :func:`DatasetImporter.__exit__`.

        Args:
            *args: the arguments to :func:`DatasetImporter.__exit__`
        """
        # Your custom code here to complete the import
        pass