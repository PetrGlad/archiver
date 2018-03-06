select sum(size) / 1000000000
from files
where path like '%/HomeMedia/%';

select count(*) from files;

select sum(size * (cnt - 1)) / 1000000000 from (
  select sha256, count(*) cnt, size, path
      from files
      where path like '%/HomeMedia/%'
      group by sha256
      having cnt > 1
      order by cnt desc);


select f.sha256, f2.size / 1024 / 1024 size_mb, f.cnt, f2.path
from (
  select sha256, count(*) cnt, size, path
    from files
    where path like '%/HomeMedia/%'
    group by sha256
    having cnt > 1
    order by size desc) f
left join files f2 where f.sha256 = f2.sha256
order by size_mb desc, f.sha256, f2.path;

