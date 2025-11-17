package app.tarea4.models;

import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

@Repository
public interface AvisoAdopcionRepository extends JpaRepository<AvisoAdopcion, Integer> {
    Page<AvisoAdopcion> findAllByOrderByIdDesc(Pageable pageable);
}
