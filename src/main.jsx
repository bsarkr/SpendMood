import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import { Auth0Provider } from '@auth0/auth0-react'
import './index.css'
import App from './App.jsx'

createRoot(document.getElementById('root')).render(
  <StrictMode>
    <Auth0Provider
      domain="dev-zqtzqntrlcy52d53.us.auth0.com"
      clientId="lFdnczk3KFaGsFY8pHt0gO9uMJn4fmlU"
      authorizationParams={{
        redirect_uri: window.location.origin,
        connection: 'SpendMood' // Add this line - must match your database name exactly
      }}
    >
      <App />
    </Auth0Provider>
  </StrictMode>,
)