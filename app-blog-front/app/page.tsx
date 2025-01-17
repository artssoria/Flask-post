'use client';
import { useEffect,useState } from "react";

interface Article{
  id : number;
  title : string;
  content : string;
}



export default function Home() {
  const [articles, setArticles] = useState<Article[]>([])
  console.log(articles)

  useEffect(() => {
    fetch('http://127.0.0.1:5000/articles')
    .then(response => response.json())
    .then(data => setArticles(data))
    .catch(error => console.error('Error al obtener los artículos:', error))
  }, [])
  



  return (
    <>
      <div>Hola mundo</div>
    </>
  );
}
