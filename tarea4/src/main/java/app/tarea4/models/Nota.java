package app.tarea4.models;

import jakarta.persistence.*;
import jakarta.validation.constraints.NotNull;

@Entity
@Table(name = "nota")
public class Nota {

    @Id
    @SequenceGenerator(
            name = "nota_seq",
            sequenceName = "nota_seq",
            allocationSize = 1
    )
    @GeneratedValue(
            strategy = GenerationType.SEQUENCE,
            generator = "nota_seq"
    )
    private Integer id;

    @ManyToOne
    @JoinColumn(name = "aviso_id", nullable = false)
    private AvisoAdopcion aviso;
    
    @NotNull
    private Integer nota;

    public Nota() {
    }

    public Nota(AvisoAdopcion aviso,
                Integer nota) {
        this.aviso = aviso;
        this.nota = nota;
    }

    public Integer getId() {
        return id;
    }

    public AvisoAdopcion getAviso() {
        return aviso;
    }

    public Integer getNota() {
        return nota;
    }
}

