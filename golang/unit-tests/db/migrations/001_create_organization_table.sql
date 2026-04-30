create table if not exists organizations (
  id serial primary key,
  name varchar(50),
  created_at timestamptz not null default now()
);
