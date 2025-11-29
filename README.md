## Refactor Notes

Tujuan refactor ini adalah menjaga behaviour aplikasi sambil memperbaiki struktur internal kode agar lebih rapi dan mudah dibaca. Seluruh endpoint, output, dan workflow tetap sama, tetapi struktur kode menggunakan pendekatan OOP.

### What Was Changed?
Kode dipisah menjadi tiga bagian yaitu EmbeddingService, DocumentStore dan RagWorkflow agar logika bisnis, penyimpanan data dan API tidak lagi bercampur dalam satu file. Struktur ini membuat alurnya lebih jelas tanpa mengubah behaviour aplikasi.

### Trade-off Considerations
Saya memilih refactor sederhana sesuai instruksi untuk tidak menambah fitur baru. Fokusnya merapikan struktur sehingga kode tetap mudah dipahami.
Hasilnya, maintainability meningkat karena setiap komponen memiliki tanggung jawab yang jelas, tidak ada lagi global state, dan proses pengujian menjadi lebih mudah. Perubahan pada satu bagian kini tidak memengaruhi bagian lainnya.

