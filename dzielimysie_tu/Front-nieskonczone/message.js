const chatItems = document.querySelectorAll('.chat-item');
  const chatHeader = document.querySelector('.chat-header h2');
  const chatMessages = document.querySelector('.chat-messages');
  const nickNameInfo = document.querySelector('.nick-name');

  chatItems.forEach((item, index) => {
    item.addEventListener('click', () => {
      // 1. Usuń klasę 'active' z wszystkich
      chatItems.forEach(i => i.classList.remove('active'));

      // 2. Dodaj 'active' do klikniętego
      item.classList.add('active');

      // 3. Przykładowa zmiana zawartości głównego okna (dynamicznie)
      const userName = `Użytkownik ${index + 1}`;
      chatHeader.textContent = userName;
      nickNameInfo.textContent = userName;
      chatMessages.innerHTML = `
        <p class="message received">Cześć, to wiadomości od ${userName}.</p>
        <p class="message sent">Hej, co mogę dla Ciebie zrobić?</p>
      `;
    });
  });

