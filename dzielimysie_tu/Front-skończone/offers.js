// Przełączanie aktywnego filtra
document.querySelectorAll('.filter').forEach(btn => {
    btn.addEventListener('click', () => {
      document.querySelectorAll('.filter').forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
    });
  });

  // Przełączanie widoku (lista / siatka)
  const listBtn = document.getElementById('listView');
  const gridBtn = document.getElementById('gridView');

  listBtn.addEventListener('click', () => {
    listBtn.classList.add('active');
    gridBtn.classList.remove('active');
    console.log('Widok: lista');
  });

  gridBtn.addEventListener('click', () => {
    gridBtn.classList.add('active');
    listBtn.classList.remove('active');
    console.log('Widok: siatka');
});