package app.tarea4.models;

import jakarta.persistence.*;
import jakarta.validation.constraints.NotNull;

import java.util.List;

@Entity
@Table(name = "region")
public class Region {

    @Id
    @SequenceGenerator(
            name = "region_seq",
            sequenceName = "region_seq",
            allocationSize = 1
    )
    @GeneratedValue(
            strategy = GenerationType.SEQUENCE,
            generator = "region_seq"
    )
    private Integer id;

    @NotNull
    private String nombre;

    @OneToMany(mappedBy = "region")
    private List<Comuna> comunas;

    public Region() {
    }

    public Integer getId() {
        return id;
    }

    public String getNombre() {
        return nombre;
    }
}
