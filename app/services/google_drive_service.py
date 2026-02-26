import io

from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload

from app.core.config import settings
from app.core.exceptions import BadRequestException

SCOPES = ["https://www.googleapis.com/auth/drive.file"]


class GoogleDriveService:
	def __init__(self) -> None:
		credentials = service_account.Credentials.from_service_account_file(
			settings.GOOGLE_SERVICE_ACCOUNT_FILE,
			scopes=SCOPES,
		)
		self._service = build("drive", "v3", credentials=credentials)

	def upload_pdf(
		self,
		pdf_bytes: bytes,
		filename: str,
		folder_id: str | None = None,
	) -> str:
		file_metadata: dict[str, object] = {"name": filename}
		if folder_id:
			file_metadata["parents"] = [folder_id]

		media = MediaIoBaseUpload(
			io.BytesIO(pdf_bytes),
			mimetype="application/pdf",
			resumable=False,
		)

		try:
			file = (
				self._service.files()
				.create(
					body=file_metadata,
					media_body=media,
					fields="id",
				)
				.execute()
			)
			return file.get("id")
		except Exception as exc:
			raise BadRequestException(
				f"Không thể upload lên Google Drive: {str(exc)}"
			) from exc
