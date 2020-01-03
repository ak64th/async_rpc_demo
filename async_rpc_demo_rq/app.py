from spyne import Application
from spyne.protocol.json import JsonDocument

from .service import DetectionService


application = Application(
    [DetectionService],
    'demo.image.detection.json',
    in_protocol=JsonDocument(validator='soft'),
    out_protocol=JsonDocument(),
)
