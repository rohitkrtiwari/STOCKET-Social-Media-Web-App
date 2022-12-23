const file = document.querySelector('#file-input');
        file.addEventListener('change', (e) => {
        const [file] = e.target.files;
        const { name: fileName, size } = file;
        const fileNameAndSize = `${fileName}`;
        document.querySelector('.file-name').textContent = fileNameAndSize;
        document.querySelector('.file-name').classList.add('file-name-active');
        });

        $(function() {
            $('#post_data').keypress(function(e) {
            var key = e.which;
            if ((event.keyCode == 10 || event.keyCode == 13) && event.ctrlKey) // the enter key code
            {
                $('#post_submit').click();
                return false;
            }
            });
        });