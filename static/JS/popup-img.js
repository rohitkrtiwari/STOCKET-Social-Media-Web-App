document.querySelectorAll('.popup-img').forEach(image => {
    image.onclick = () => {
        document.querySelector('.popup-image').style.width = '100%';
        document.querySelector('.popup-image').style.height = '100%';
        document.querySelector('#popup-span').style.display = 'block';
        document.querySelector('.popup-image img').src = image.getAttribute('src');
    }
});
document.querySelector('#popup-span').onclick = () => {
        document.querySelector('#popup-span').style.display = 'none';
        document.querySelector('.popup-image').style.width = '0%';
    document.querySelector('.popup-image').style.height = '0%';
}