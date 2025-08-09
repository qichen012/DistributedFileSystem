create table files(
    id int auto_increment primary key,
    file_name varchar(255) not null,
    filesize bigint not null,
    upload_time datetime deafault current_timestamp
);
create table chunks(
    id int auto_increment primary key,
    file_id int not null,
    chunk_index int not null,
    check_sum varchar(64),
    node_address varchar(255),
    foreign key (file_id) references files (id)
);
create table storage_nodes(
    id int auto_increment primary key,
    address_sn varchar(255) not null,
    last_heartbeat datetime
);