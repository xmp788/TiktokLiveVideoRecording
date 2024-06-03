maping={
  get_a_bogus:function(params,Path,userAgent) {
  if(Path){
      // 如果是python调用
      require(`${Path}/cd_crypt/environment.js`);
      require(`${Path}/cd_crypt/source.js`);
    }else{
      // 如果是同路径js调用
      require('./environment.js');
      require('./source.js');
      userAgent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.6261.95 Safari/537.36'
    }
    const arguments = [0, 1, 14, params, "", userAgent]
    let r = window.a_b._v;
    // return 'dJm0MdufDDdTXDW656oLfY3q63F3Y83-0trEMD2fWn3p5g39HMP-9exoIF0vYhYjLG/lIeLjy4hjTNPME5/jA3J1HmJNU2KZ-gYZt-P2so0j53intL6mE0hN5vb3SFlm5XNAEOJ0y7cezSRDloFe-wHvPjojx2f39gbR'
    return (0, window.a_b._u)(r[0], arguments, r[1], r[2], this)
  }
};