drop table if exists images;
create table images (
	id integer primary key autoincrement,
	link text not null,
	title text not null,
	caption text not null,
	type text not null,
	width text not null,
	height text not null,
	alt text not null
)