package app.tarea4.models;

import jakarta.persistence.*;
import jakarta.validation.constraints.NotNull;

import java.util.List;

@Entity
@Table(name = "comuna")
public class Comuna {

    @Id
    @SequenceGenerator(
            name = "comuna_seq",
            sequenceName = "comuna_seq",
            allocationSize = 1
    )
    @GeneratedValue(
            strategy = GenerationType.SEQUENCE,
            generator = "comuna_seq"
    )
    private Integer id;

    @NotNull
    private String nombre;

    @ManyToOne
    @JoinColumn(name = "region_id", nullable = false)
    private Region region;

    @OneToMany(mappedBy = "comuna")
    private List<AvisoAdopcion> avisosAdopcion;

    public Comuna() {
    }

    public Integer getId() {
        return id;
    }

    public String getNombre() {
        return nombre;
    }

    public Region getRegion() {
        return region;
    }
}
