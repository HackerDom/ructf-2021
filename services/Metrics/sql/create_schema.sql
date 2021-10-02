create schema if not exists ru_ctf_schema;
drop table if exists ru_ctf_schema.tbl_metric;
create table if not exists ru_ctf_schema.tbl_metric (
    token varchar(255) primary key,
    device varchar(255),
    type varchar(255),
    metainfo varchar(255),
    value int,
    creationTime timestamp,
    info varchar(255)
);