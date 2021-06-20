from .administrator import AdministratorRegister, AdministratorList, AdministratorDetail
from .dean_worker import DeanWorkerRegister, DeanWorkerList, DeanWorkerDetail
from .promoter import PromoterBulkDelete, PromoterBulkRegister, PromoterRegister, PromoterList, PromoterDetail, PromoterListForRecord, PromoterDetailForRecord
from .student import StudentBulkDelete, StudentBulkRegister, StudentRegister, StudentList, StudentDetail
from .user import Login, UserChangePassword, UserDetail
from .file import FileAdd, FileList, FileDetail
from .index import index
from .record import GetElectionsStatus, RecordListForPromoter, RecordDetailForPromoter, RecordListForStudent, RecordDetailForStudent, RecordListSummary, RevokeRecords, RecordListSummaryToCsvFile
