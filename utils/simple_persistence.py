import json
from datetime import datetime, timezone, timedelta
from pathlib import Path
from utils import Logger

class SimplePersistence:
    """
    This class is meant to build a simple persistence module for storing and loading submissions.
    """
    
    def __init__(self, base_path: str, logger:Logger) -> None:
        """
        Initialize the persistence module.

        :param base_path: Base directory for storing submissions.
        :type base_path: str
        :param logger: Logger instance for logging messages.
        :type logger: utils.Logger
        """
        
        self.base_path = Path(base_path)
        self.logger = logger
        self.base_path.mkdir(exist_ok=True)

        self.metadata_file = self.base_path / "metadata.json"
        if not self.metadata_file.exists():
            with self.metadata_file.open("w", encoding="utf-8") as f:
                json.dump({}, f)  # start with an empty dict

    def _load_metadata(self) -> dict:
        """
        Load the entire metadata.json as a Python dict.
        If it does not exist or is invalid, return an empty dict.

        :return: A dictionary containing all metadata entries.
        :rtype: dict
        """
        try:
            with self.metadata_file.open("r", encoding="utf-8") as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            self.logger.warning(f"Cannot load metadata.json properly, returning empty metadata. Error: {e}")
            return {}

    def _save_metadata(self, metadata: dict) -> None:
        """
        Save the metadata dict back to metadata.json.

        :param metadata: A dictionary containing all metadata entries to be saved.
        :type metadata: dict
        :return: None
        :rtype: None
        """
        with self.metadata_file.open("w", encoding="utf-8") as f:
            json.dump(metadata, f, indent=2)

    def store_submission(self, submission_id: str, payload: list[str]) -> None:
        """
        Store a submission with a given ID and payload (list of strings).
        
        1) Creates a file named <submission_id>.txt in base_path.
        2) Updates metadata.json with submission's info (date of indexing, etc.).

        :param submission_id: Unique identifier for the submission.
        :type submission_id: str
        :param payload: The list of strings representing the submission data.
        :type payload: list[str]
        :return: None
        :rtype: None
        """
        payload_file = self.base_path / f"{submission_id}.txt"
        with payload_file.open("w", encoding="utf-8") as f:
            for line in payload:
                f.write(line + "\n")

        metadata = self._load_metadata()
        metadata[submission_id] = {"date_indexed": datetime.now(timezone.utc).isoformat()}
        self._save_metadata(metadata)
        
        self.cleanup_submissions()

        self.logger.info(f"Stored submission '{submission_id}' in '{payload_file}'.")

    def load_submission(self, submission_id: str) -> dict:
        """
        Load a submission by its ID.
        
        :param submission_id: Unique identifier for the submission.
        :type submission_id: str
        :return: A dictionary with 'payload' (list of strings) and 'metadata' (dict).
        :rtype: dict
        :raises FileNotFoundError: If the .txt file or metadata entry does not exist.
        """
        payload_file = self.base_path / f"{submission_id}.txt"
        if not payload_file.exists():
            self.logger.error(f"Submission file '{submission_id}.txt' not found.")
            raise FileNotFoundError(f"Submission file '{submission_id}.txt' does not exist.")

        with payload_file.open("r", encoding="utf-8") as f:
            payload = [line.rstrip("\n") for line in f]

        metadata = self._load_metadata()
        if submission_id not in metadata:
            self.logger.error(f"No metadata for submission '{submission_id}' in metadata.json.")
            raise FileNotFoundError(f"No metadata for submission '{submission_id}'.")

        submission_metadata = metadata[submission_id]
        self.logger.info(f"Loaded submission '{submission_id}'.")
        
        self.cleanup_submissions()
        
        return {
            "payload": payload,
            "metadata": submission_metadata
        }


    def load_only_payload(self, submission_id: str) -> list[str]:
        """
        Load only the payload (list of strings) for a given submission ID.

        :param submission_id: Unique identifier for the submission.
        :type submission_id: str
        :return: A list of strings representing the submission's payload.
        :rtype: list[str]
        :raises FileNotFoundError: If the submission file or metadata entry does not exist.
        """
        submission_data = self.load_submission(submission_id)
        return submission_data["payload"]
        
    
    def cleanup_submissions(self, older_than_days: int = 28) -> None:
        """
        Delete submissions older than the specified number of days.
        
        1) Loads metadata from metadata.json.
        2) Finds submissions whose 'date_indexed' is older than the cutoff.
        3) Deletes those submissions' .txt files.
        4) Removes them from the metadata.json.

        :param older_than_days: Number of days beyond which submissions are considered old.
        :type older_than_days: int
        :return: None
        :rtype: None
        """
        self.logger.info(f"Cleaning up submissions older than {older_than_days} days...")
        metadata = self._load_metadata()
        cutoff_date = datetime.now(timezone.utc) - timedelta(days=older_than_days)

        to_delete = []

        # Identify which submissions should be removed
        for submission_id, data in metadata.items():
            date_str = data.get("date_indexed")
            if not date_str:
                self.logger.warning(
                    f"No 'date_indexed' for submission '{submission_id}', skipping."
                )
                continue

            try:
                date_indexed = datetime.fromisoformat(date_str)
            except ValueError as e:
                self.logger.warning(
                    f"Cannot parse date for '{submission_id}' (value: {date_str}). Error: {e}"
                )
                continue

            if date_indexed < cutoff_date:
                to_delete.append(submission_id)

        # Perform deletions
        for submission_id in to_delete:
            file_path = self.base_path / f"{submission_id}.txt"
            if file_path.exists():
                file_path.unlink()  # delete the file
                self.logger.info(f"Deleted file '{file_path}' for old submission '{submission_id}'.")

            # Remove from metadata
            del metadata[submission_id]

        # Save updated metadata
        self._save_metadata(metadata)

        if to_delete:
            self.logger.info(f"Deleted {len(to_delete)} submissions older than {older_than_days} days.")
        else:
            self.logger.info("No old submissions found to delete.")