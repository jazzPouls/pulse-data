# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: ingest_info.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='ingest_info.proto',
  package='recidiviz.ingest.models',
  syntax='proto2',
  serialized_options=None,
  serialized_pb=_b('\n\x11ingest_info.proto\x12\x17recidiviz.ingest.models\"\xb9\x02\n\nIngestInfo\x12/\n\x06people\x18\x01 \x03(\x0b\x32\x1f.recidiviz.ingest.models.Person\x12\x32\n\x08\x62ookings\x18\x02 \x03(\x0b\x32 .recidiviz.ingest.models.Booking\x12\x30\n\x07\x63harges\x18\x03 \x03(\x0b\x32\x1f.recidiviz.ingest.models.Charge\x12,\n\x05\x62onds\x18\x04 \x03(\x0b\x32\x1d.recidiviz.ingest.models.Bond\x12\x30\n\x07\x61rrests\x18\x05 \x03(\x0b\x32\x1f.recidiviz.ingest.models.Arrest\x12\x34\n\tsentences\x18\x06 \x03(\x0b\x32!.recidiviz.ingest.models.Sentence\"\xd6\x01\n\x06Person\x12\x11\n\tperson_id\x18\x01 \x01(\t\x12\x0f\n\x07surname\x18\x02 \x01(\t\x12\x13\n\x0bgiven_names\x18\x03 \x01(\t\x12\x11\n\tbirthdate\x18\x04 \x01(\t\x12\x0e\n\x06gender\x18\x05 \x01(\t\x12\x0b\n\x03\x61ge\x18\x06 \x01(\t\x12\x0c\n\x04race\x18\x07 \x01(\t\x12\x11\n\tethnicity\x18\x08 \x01(\t\x12\x1a\n\x12place_of_residence\x18\t \x01(\t\x12\x11\n\tfull_name\x18\n \x01(\t\x12\x13\n\x0b\x62ooking_ids\x18\x0b \x03(\t\"\x95\x02\n\x07\x42ooking\x12\x12\n\nbooking_id\x18\x01 \x01(\t\x12\x16\n\x0e\x61\x64mission_date\x18\x02 \x01(\t\x12\x1e\n\x16projected_release_date\x18\x03 \x01(\t\x12\x14\n\x0crelease_date\x18\x04 \x01(\t\x12\x16\n\x0erelease_reason\x18\x05 \x01(\t\x12\x16\n\x0e\x63ustody_status\x18\x06 \x01(\t\x12\x0c\n\x04hold\x18\x07 \x01(\t\x12\x10\n\x08\x66\x61\x63ility\x18\x08 \x01(\t\x12\x16\n\x0e\x63lassification\x18\t \x01(\t\x12\x19\n\x11total_bond_amount\x18\n \x01(\t\x12\x11\n\tarrest_id\x18\x0b \x01(\t\x12\x12\n\ncharge_ids\x18\x0c \x03(\t\"u\n\x06\x41rrest\x12\x11\n\tarrest_id\x18\x01 \x01(\t\x12\x0c\n\x04\x64\x61te\x18\x02 \x01(\t\x12\x10\n\x08location\x18\x03 \x01(\t\x12\x14\n\x0cofficer_name\x18\x04 \x01(\t\x12\x12\n\nofficer_id\x18\x05 \x01(\t\x12\x0e\n\x06\x61gency\x18\x06 \x01(\t\"\xec\x02\n\x06\x43harge\x12\x11\n\tcharge_id\x18\x01 \x01(\t\x12\x14\n\x0coffense_date\x18\x02 \x01(\t\x12\x0f\n\x07statute\x18\x03 \x01(\t\x12\x0c\n\x04name\x18\x04 \x01(\t\x12\x11\n\tattempted\x18\x05 \x01(\t\x12\x0e\n\x06\x64\x65gree\x18\x06 \x01(\t\x12\x14\n\x0c\x63harge_class\x18\x07 \x01(\t\x12\r\n\x05level\x18\x08 \x01(\t\x12\x13\n\x0b\x66\x65\x65_dollars\x18\t \x01(\t\x12\x17\n\x0f\x63harging_entity\x18\n \x01(\t\x12\x0e\n\x06status\x18\x0b \x01(\t\x12\x18\n\x10number_of_counts\x18\x0c \x01(\t\x12\x12\n\ncourt_type\x18\r \x01(\t\x12\x13\n\x0b\x63\x61se_number\x18\x0e \x01(\t\x12\x17\n\x0fnext_court_date\x18\x0f \x01(\t\x12\x12\n\njudge_name\x18\x10 \x01(\t\x12\x0f\n\x07\x62ond_id\x18\x11 \x01(\t\x12\x13\n\x0bsentence_id\x18\x12 \x01(\t\"J\n\x04\x42ond\x12\x0f\n\x07\x62ond_id\x18\x01 \x01(\t\x12\x0e\n\x06\x61mount\x18\x02 \x01(\t\x12\x11\n\tbond_type\x18\x03 \x01(\t\x12\x0e\n\x06status\x18\x04 \x01(\t\"\x8d\x02\n\x08Sentence\x12\x13\n\x0bsentence_id\x18\x01 \x01(\t\x12\x14\n\x0c\x64\x61te_imposed\x18\x02 \x01(\t\x12\x12\n\nmin_length\x18\x03 \x01(\t\x12\x12\n\nmax_length\x18\x04 \x01(\t\x12\x0f\n\x07is_life\x18\x05 \x01(\t\x12\x14\n\x0cis_probation\x18\x06 \x01(\t\x12\x14\n\x0cis_suspended\x18\x07 \x01(\t\x12\x14\n\x0c\x66ine_dollars\x18\x08 \x01(\t\x12\x17\n\x0fparole_possible\x18\t \x01(\t\x12\'\n\x1fpost_release_supervision_length\x18\n \x01(\t\x12\x19\n\x11sentencing_region\x18\x0b \x01(\t')
)




_INGESTINFO = _descriptor.Descriptor(
  name='IngestInfo',
  full_name='recidiviz.ingest.models.IngestInfo',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='people', full_name='recidiviz.ingest.models.IngestInfo.people', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='bookings', full_name='recidiviz.ingest.models.IngestInfo.bookings', index=1,
      number=2, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='charges', full_name='recidiviz.ingest.models.IngestInfo.charges', index=2,
      number=3, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='bonds', full_name='recidiviz.ingest.models.IngestInfo.bonds', index=3,
      number=4, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='arrests', full_name='recidiviz.ingest.models.IngestInfo.arrests', index=4,
      number=5, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='sentences', full_name='recidiviz.ingest.models.IngestInfo.sentences', index=5,
      number=6, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=47,
  serialized_end=360,
)


_PERSON = _descriptor.Descriptor(
  name='Person',
  full_name='recidiviz.ingest.models.Person',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='person_id', full_name='recidiviz.ingest.models.Person.person_id', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='surname', full_name='recidiviz.ingest.models.Person.surname', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='given_names', full_name='recidiviz.ingest.models.Person.given_names', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='birthdate', full_name='recidiviz.ingest.models.Person.birthdate', index=3,
      number=4, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='gender', full_name='recidiviz.ingest.models.Person.gender', index=4,
      number=5, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='age', full_name='recidiviz.ingest.models.Person.age', index=5,
      number=6, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='race', full_name='recidiviz.ingest.models.Person.race', index=6,
      number=7, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='ethnicity', full_name='recidiviz.ingest.models.Person.ethnicity', index=7,
      number=8, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='place_of_residence', full_name='recidiviz.ingest.models.Person.place_of_residence', index=8,
      number=9, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='full_name', full_name='recidiviz.ingest.models.Person.full_name', index=9,
      number=10, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='booking_ids', full_name='recidiviz.ingest.models.Person.booking_ids', index=10,
      number=11, type=9, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=363,
  serialized_end=577,
)


_BOOKING = _descriptor.Descriptor(
  name='Booking',
  full_name='recidiviz.ingest.models.Booking',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='booking_id', full_name='recidiviz.ingest.models.Booking.booking_id', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='admission_date', full_name='recidiviz.ingest.models.Booking.admission_date', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='projected_release_date', full_name='recidiviz.ingest.models.Booking.projected_release_date', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='release_date', full_name='recidiviz.ingest.models.Booking.release_date', index=3,
      number=4, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='release_reason', full_name='recidiviz.ingest.models.Booking.release_reason', index=4,
      number=5, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='custody_status', full_name='recidiviz.ingest.models.Booking.custody_status', index=5,
      number=6, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='hold', full_name='recidiviz.ingest.models.Booking.hold', index=6,
      number=7, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='facility', full_name='recidiviz.ingest.models.Booking.facility', index=7,
      number=8, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='classification', full_name='recidiviz.ingest.models.Booking.classification', index=8,
      number=9, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='total_bond_amount', full_name='recidiviz.ingest.models.Booking.total_bond_amount', index=9,
      number=10, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='arrest_id', full_name='recidiviz.ingest.models.Booking.arrest_id', index=10,
      number=11, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='charge_ids', full_name='recidiviz.ingest.models.Booking.charge_ids', index=11,
      number=12, type=9, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=580,
  serialized_end=857,
)


_ARREST = _descriptor.Descriptor(
  name='Arrest',
  full_name='recidiviz.ingest.models.Arrest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='arrest_id', full_name='recidiviz.ingest.models.Arrest.arrest_id', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='date', full_name='recidiviz.ingest.models.Arrest.date', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='location', full_name='recidiviz.ingest.models.Arrest.location', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='officer_name', full_name='recidiviz.ingest.models.Arrest.officer_name', index=3,
      number=4, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='officer_id', full_name='recidiviz.ingest.models.Arrest.officer_id', index=4,
      number=5, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='agency', full_name='recidiviz.ingest.models.Arrest.agency', index=5,
      number=6, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=859,
  serialized_end=976,
)


_CHARGE = _descriptor.Descriptor(
  name='Charge',
  full_name='recidiviz.ingest.models.Charge',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='charge_id', full_name='recidiviz.ingest.models.Charge.charge_id', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='offense_date', full_name='recidiviz.ingest.models.Charge.offense_date', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='statute', full_name='recidiviz.ingest.models.Charge.statute', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='name', full_name='recidiviz.ingest.models.Charge.name', index=3,
      number=4, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='attempted', full_name='recidiviz.ingest.models.Charge.attempted', index=4,
      number=5, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='degree', full_name='recidiviz.ingest.models.Charge.degree', index=5,
      number=6, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='charge_class', full_name='recidiviz.ingest.models.Charge.charge_class', index=6,
      number=7, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='level', full_name='recidiviz.ingest.models.Charge.level', index=7,
      number=8, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='fee_dollars', full_name='recidiviz.ingest.models.Charge.fee_dollars', index=8,
      number=9, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='charging_entity', full_name='recidiviz.ingest.models.Charge.charging_entity', index=9,
      number=10, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='status', full_name='recidiviz.ingest.models.Charge.status', index=10,
      number=11, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='number_of_counts', full_name='recidiviz.ingest.models.Charge.number_of_counts', index=11,
      number=12, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='court_type', full_name='recidiviz.ingest.models.Charge.court_type', index=12,
      number=13, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='case_number', full_name='recidiviz.ingest.models.Charge.case_number', index=13,
      number=14, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='next_court_date', full_name='recidiviz.ingest.models.Charge.next_court_date', index=14,
      number=15, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='judge_name', full_name='recidiviz.ingest.models.Charge.judge_name', index=15,
      number=16, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='bond_id', full_name='recidiviz.ingest.models.Charge.bond_id', index=16,
      number=17, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='sentence_id', full_name='recidiviz.ingest.models.Charge.sentence_id', index=17,
      number=18, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=979,
  serialized_end=1343,
)


_BOND = _descriptor.Descriptor(
  name='Bond',
  full_name='recidiviz.ingest.models.Bond',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='bond_id', full_name='recidiviz.ingest.models.Bond.bond_id', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='amount', full_name='recidiviz.ingest.models.Bond.amount', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='bond_type', full_name='recidiviz.ingest.models.Bond.bond_type', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='status', full_name='recidiviz.ingest.models.Bond.status', index=3,
      number=4, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=1345,
  serialized_end=1419,
)


_SENTENCE = _descriptor.Descriptor(
  name='Sentence',
  full_name='recidiviz.ingest.models.Sentence',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='sentence_id', full_name='recidiviz.ingest.models.Sentence.sentence_id', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='date_imposed', full_name='recidiviz.ingest.models.Sentence.date_imposed', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='min_length', full_name='recidiviz.ingest.models.Sentence.min_length', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='max_length', full_name='recidiviz.ingest.models.Sentence.max_length', index=3,
      number=4, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='is_life', full_name='recidiviz.ingest.models.Sentence.is_life', index=4,
      number=5, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='is_probation', full_name='recidiviz.ingest.models.Sentence.is_probation', index=5,
      number=6, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='is_suspended', full_name='recidiviz.ingest.models.Sentence.is_suspended', index=6,
      number=7, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='fine_dollars', full_name='recidiviz.ingest.models.Sentence.fine_dollars', index=7,
      number=8, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='parole_possible', full_name='recidiviz.ingest.models.Sentence.parole_possible', index=8,
      number=9, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='post_release_supervision_length', full_name='recidiviz.ingest.models.Sentence.post_release_supervision_length', index=9,
      number=10, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='sentencing_region', full_name='recidiviz.ingest.models.Sentence.sentencing_region', index=10,
      number=11, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=1422,
  serialized_end=1691,
)

_INGESTINFO.fields_by_name['people'].message_type = _PERSON
_INGESTINFO.fields_by_name['bookings'].message_type = _BOOKING
_INGESTINFO.fields_by_name['charges'].message_type = _CHARGE
_INGESTINFO.fields_by_name['bonds'].message_type = _BOND
_INGESTINFO.fields_by_name['arrests'].message_type = _ARREST
_INGESTINFO.fields_by_name['sentences'].message_type = _SENTENCE
DESCRIPTOR.message_types_by_name['IngestInfo'] = _INGESTINFO
DESCRIPTOR.message_types_by_name['Person'] = _PERSON
DESCRIPTOR.message_types_by_name['Booking'] = _BOOKING
DESCRIPTOR.message_types_by_name['Arrest'] = _ARREST
DESCRIPTOR.message_types_by_name['Charge'] = _CHARGE
DESCRIPTOR.message_types_by_name['Bond'] = _BOND
DESCRIPTOR.message_types_by_name['Sentence'] = _SENTENCE
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

IngestInfo = _reflection.GeneratedProtocolMessageType('IngestInfo', (_message.Message,), dict(
  DESCRIPTOR = _INGESTINFO,
  __module__ = 'ingest_info_pb2'
  # @@protoc_insertion_point(class_scope:recidiviz.ingest.models.IngestInfo)
  ))
_sym_db.RegisterMessage(IngestInfo)

Person = _reflection.GeneratedProtocolMessageType('Person', (_message.Message,), dict(
  DESCRIPTOR = _PERSON,
  __module__ = 'ingest_info_pb2'
  # @@protoc_insertion_point(class_scope:recidiviz.ingest.models.Person)
  ))
_sym_db.RegisterMessage(Person)

Booking = _reflection.GeneratedProtocolMessageType('Booking', (_message.Message,), dict(
  DESCRIPTOR = _BOOKING,
  __module__ = 'ingest_info_pb2'
  # @@protoc_insertion_point(class_scope:recidiviz.ingest.models.Booking)
  ))
_sym_db.RegisterMessage(Booking)

Arrest = _reflection.GeneratedProtocolMessageType('Arrest', (_message.Message,), dict(
  DESCRIPTOR = _ARREST,
  __module__ = 'ingest_info_pb2'
  # @@protoc_insertion_point(class_scope:recidiviz.ingest.models.Arrest)
  ))
_sym_db.RegisterMessage(Arrest)

Charge = _reflection.GeneratedProtocolMessageType('Charge', (_message.Message,), dict(
  DESCRIPTOR = _CHARGE,
  __module__ = 'ingest_info_pb2'
  # @@protoc_insertion_point(class_scope:recidiviz.ingest.models.Charge)
  ))
_sym_db.RegisterMessage(Charge)

Bond = _reflection.GeneratedProtocolMessageType('Bond', (_message.Message,), dict(
  DESCRIPTOR = _BOND,
  __module__ = 'ingest_info_pb2'
  # @@protoc_insertion_point(class_scope:recidiviz.ingest.models.Bond)
  ))
_sym_db.RegisterMessage(Bond)

Sentence = _reflection.GeneratedProtocolMessageType('Sentence', (_message.Message,), dict(
  DESCRIPTOR = _SENTENCE,
  __module__ = 'ingest_info_pb2'
  # @@protoc_insertion_point(class_scope:recidiviz.ingest.models.Sentence)
  ))
_sym_db.RegisterMessage(Sentence)


# @@protoc_insertion_point(module_scope)
