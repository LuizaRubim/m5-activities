import clsx from 'clsx';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import Layout from '@theme/Layout';

import Heading from '@theme/Heading';
import styles from './index.module.css';

function HomepageHeader() {
  return (
    <header className={clsx('hero hero--primary', styles.heroBanner)}>
      <div className="container">
        <Heading as="h1" className="hero__title">Rubim resenhas</Heading>
        <p className="hero__subtitle"> Minhas opiniões claramente duvidosas sobre o mundo da ficção</p>
      </div>
    </header>
  );
}

export default function Home() {
  const {siteConfig} = useDocusaurusContext();
  return (
    <Layout>
      <HomepageHeader />
      <main>
        <div className={clsx('body_main', styles.bodyMain)}><h2>Em breve...</h2></div>
      </main>
    </Layout>
  );
}
