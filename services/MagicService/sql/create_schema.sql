create schema if not exists ru_ctf_schema;
create table if not exists ru_ctf_schema.tbl_metric (
    token bigint primary key,
    device varchar (255),
    type varchar (255),
    metainfo varchar (255)
);

